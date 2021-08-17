from json.decoder import JSONDecoder
import os
import requests

from typing import Optional
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse


BASE_URL = os.getenv("BASE_URL", "http://example.com")

app = FastAPI()


def build_url(path):
    return f'{BASE_URL}/{path}'


def build_headers(request):
    headers = dict(request.headers)
    accept = headers.get('accept')
    content_type = headers.get('content-type')
    headers = {
        'X-Api-Key': headers.get('x-api-key')
    }

    if accept:
        headers['Accept'] = accept

    if content_type:
        headers['Content-Type'] = content_type

    return headers


@app.get("/{path:path}")
def get(path, request: Request):
    url = build_url(path)
    headers = build_headers(request)
    response = requests.get(url, params=dict(request.query_params), headers=headers)
    return JSONResponse(response.json(), status_code=response.status_code)


@app.post("/{path:path}")
def post(path, request: Request):
    url = build_url(path)
    headers = build_headers(request)
    response = requests.post(
        url, json=request.data, params=request.query_params, headers=headers)
    return JSONResponse(response.json(), status_code=response.status_code)


@app.put("/{path:path}")
def put(path, request):
    url = build_url(path)
    headers = build_headers(request)
    response = requests.put(url, json=request.data,
                            params=request.query_params, headers=headers)
    return Response(response.json(), status_code=response.status_code)


@app.put("/{path:path}")
def delete(path, request):
    url = build_url(path)
    headers = build_headers(request)
    response = requests.delete(
        url, params=request.query_params, headers=headers)
    return Response(response.json(), status_code=response.status_code)
