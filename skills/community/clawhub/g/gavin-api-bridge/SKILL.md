---
name: api-bridge
description: "Generate API integrations from OpenAPI/Swagger specs. Auto-create MCP servers, API clients, and webhook handlers. Use when user wants to connect to a REST API, generate an API client, create an MCP server from an OpenAPI spec, or scaffold API integrations."
version: 2.0.0
author: lrg913427-dot
license: MIT
metadata:
  hermes:
    tags: [api, openapi, swagger, mcp, integration, scaffolding, rest, webhook, client]
    related_skills: [db-explorer, native-mcp]
---

# API Bridge

Generate API integrations from OpenAPI/Swagger specs — MCP servers, API clients, and webhook handlers.

## When to Use

Activate this skill when the user:
- Says "connect to this API", "integrate with X", "build an API client"
- Wants to create an MCP server for a REST API
- Has an OpenAPI/Swagger spec and wants code generated
- Needs a webhook handler for API events
- Wants to scaffold an API integration quickly
- Mentions "API key", "REST endpoint", or "webhook"

## What This Skill Does

When a user wants to connect to an API, this skill:
1. Finds or fetches the OpenAPI/Swagger spec
2. Generates a working MCP server or API client
3. Handles auth (API key, OAuth2, Bearer token)
4. Includes error handling, rate limiting, and retries
5. Produces ready-to-use code

## Quick Start

### From OpenAPI Spec URL

```bash
# Fetch the spec
curl -s https://api.example.com/openapi.json > /tmp/api-spec.json

# Generate MCP server
# (Use the steps below)
```

### From Existing API Documentation

If no OpenAPI spec exists, create one from the API docs:
1. Identify base URL and endpoints
2. Create a minimal OpenAPI 3.0 spec
3. Generate the integration

## Step 1: Parse the Spec

```python
import json

with open('api-spec.json') as f:
    spec = json.load(f)

info = spec.get('info', {})
base_url = spec.get('servers', [{}])[0].get('url', '')
paths = spec.get('paths', {})

print(f"API: {info.get('title')}")
print(f"Version: {info.get('version')}")
print(f"Base URL: {base_url}")
print(f"Endpoints: {len(paths)}")

# List all endpoints
for path, methods in paths.items():
    for method in methods:
        if method in ['get', 'post', 'put', 'patch', 'delete']:
            print(f"  {method.upper()} {path}")
```

## Step 2: Generate MCP Server (Python)

```python
# mcp_server.py - Generated from OpenAPI spec
import os
import json
import httpx
from mcp.server import Server
from mcp.types import Tool, TextContent

app = Server("api-name")

BASE_URL = "https://api.example.com"
API_KEY = os.environ.get("API_KEY", "")

@app.tool()
async def list_items(limit: int = 10) -> str:
    """List items from the API."""
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"{BASE_URL}/items",
            headers={"Authorization": f"Bearer {API_KEY}"},
            params={"limit": limit},
        )
        resp.raise_for_status()
        return json.dumps(resp.json(), indent=2)

@app.tool()
async def get_item(item_id: str) -> str:
    """Get a single item by ID."""
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"{BASE_URL}/items/{item_id}",
            headers={"Authorization": f"Bearer {API_KEY}"},
        )
        resp.raise_for_status()
        return json.dumps(resp.json(), indent=2)

@app.tool()
async def create_item(name: str, description: str = "") -> str:
    """Create a new item."""
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{BASE_URL}/items",
            headers={"Authorization": f"Bearer {API_KEY}"},
            json={"name": name, "description": description},
        )
        resp.raise_for_status()
        return json.dumps(resp.json(), indent=2)
```

## Step 3: Add Rate Limiting

```python
import asyncio
from collections import deque
import time

class RateLimiter:
    def __init__(self, max_requests: int = 100, window: int = 60):
        self.max_requests = max_requests
        self.window = window
        self.timestamps = deque()

    async def acquire(self):
        now = time.time()
        while self.timestamps and now - self.timestamps[0] > self.window:
            self.timestamps.popleft()

        if len(self.timestamps) >= self.max_requests:
            wait = self.window - (now - self.timestamps[0])
            await asyncio.sleep(wait)

        self.timestamps.append(time.time())

rate_limiter = RateLimiter(max_requests=100, window=60)
```

## Step 4: Add Retry Logic

```python
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=10),
)
async def api_request(method: str, path: str, **kwargs) -> dict:
    """Make an API request with retry logic."""
    async with httpx.AsyncClient() as client:
        resp = await client.request(
            method,
            f"{BASE_URL}{path}",
            headers={"Authorization": f"Bearer {API_KEY}"},
            **kwargs,
        )
        resp.raise_for_status()
        return resp.json()
```

## Generate Python API Client

```python
"""API client generated from OpenAPI spec."""

import httpx
from typing import Optional, Dict, Any


class APIClient:
    def __init__(self, base_url: str, api_key: str = ""):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self._client = httpx.AsyncClient(
            base_url=self.base_url,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            timeout=30.0,
        )

    async def close(self):
        await self._client.aclose()

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        await self.close()

    async def _request(
        self,
        method: str,
        path: str,
        params: Optional[Dict] = None,
        json: Optional[Dict] = None,
    ) -> Any:
        resp = await self._client.request(method, path, params=params, json=json)
        resp.raise_for_status()
        return resp.json()

    # Generated methods from OpenAPI spec
    async def list_items(self, limit: int = 10) -> list:
        return await self._request("GET", "/items", params={"limit": limit})

    async def get_item(self, item_id: str) -> dict:
        return await self._request("GET", f"/items/{item_id}")

    async def create_item(self, name: str, **kwargs) -> dict:
        return await self._request("POST", "/items", json={"name": name, **kwargs})

    async def update_item(self, item_id: str, **kwargs) -> dict:
        return await self._request("PATCH", f"/items/{item_id}", json=kwargs)

    async def delete_item(self, item_id: str) -> None:
        await self._request("DELETE", f"/items/{item_id}")
```

## Generate Webhook Handler

```python
"""Webhook handler for API events."""

from fastapi import FastAPI, Request, HTTPException
import hmac
import hashlib

app = FastAPI()
WEBHOOK_SECRET = os.environ.get("WEBHOOK_SECRET", "")

@app.post("/webhook")
async def handle_webhook(request: Request):
    # Verify signature
    body = await request.body()
    signature = request.headers.get("X-Signature", "")

    expected = hmac.new(
        WEBHOOK_SECRET.encode(),
        body,
        hashlib.sha256,
    ).hexdigest()

    if not hmac.compare_digest(signature, expected):
        raise HTTPException(status_code=401, detail="Invalid signature")

    payload = await request.json()
    event_type = payload.get("event_type")

    if event_type == "item.created":
        await handle_item_created(payload)
    elif event_type == "item.updated":
        await handle_item_updated(payload)
    elif event_type == "item.deleted":
        await handle_item_deleted(payload)

    return {"status": "ok"}
```

## Common API Patterns

### OAuth2 Flow

```python
async def get_oauth_token(
    client_id: str,
    client_secret: str,
    token_url: str,
) -> str:
    """Get OAuth2 access token."""
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            token_url,
            data={
                "grant_type": "client_credentials",
                "client_id": client_id,
                "client_secret": client_secret,
            },
        )
        resp.raise_for_status()
        return resp.json()["access_token"]
```

### Pagination

```python
async def list_all_items(api_client) -> list:
    """List all items with automatic pagination."""
    all_items = []
    cursor = None

    while True:
        params = {"limit": 100}
        if cursor:
            params["cursor"] = cursor

        result = await api_client._request("GET", "/items", params=params)
        all_items.extend(result["data"])

        cursor = result.get("next_cursor")
        if not cursor:
            break

    return all_items
```

### File Upload

```python
async def upload_file(api_client, file_path: str) -> dict:
    """Upload a file to the API."""
    async with httpx.AsyncClient() as client:
        with open(file_path, "rb") as f:
            resp = await client.post(
                f"{api_client.base_url}/files",
                headers={"Authorization": f"Bearer {api_client.api_key}"},
                files={"file": (file_path, f, "application/octet-stream")},
            )
            resp.raise_for_status()
            return resp.json()
```

## OpenAPI Spec Sources

Common places to find OpenAPI specs:

| API | Spec URL |
|-----|----------|
| GitHub | https://api.github.com/openapi.json |
| Stripe | https://raw.githubusercontent.com/stripe/openapi/master/openapi/spec3.json |
| Twilio | https://github.com/twilio/twilio-oai/blob/main/spec/yaml/twilio_api_v2010.yaml |
| OpenAI | https://github.com/openai/openai-openapi/blob/main/openapi.yaml |
| Notion | https://github.com/makenotion/notion-sdk-js/blob/main/api-openapi.yml |

Or search: `site:github.com "openapi" OR "swagger" "api-name"`

## Pitfalls

- **Spec version** — Check if it's OpenAPI 2.0 (Swagger) or 3.0+ (different format)
- **Auth types** — API key vs Bearer token vs OAuth2 vs Basic auth (check spec's securitySchemes)
- **Rate limits** — Always implement rate limiting; check API docs for limits
- **Pagination** — Different APIs use different patterns (cursor, offset, page, link header)
- **Content types** — Some APIs use `application/x-www-form-urlencoded` instead of JSON
- **Webhook verification** — Always verify signatures; don't trust raw payloads
- **Error handling** — Check API docs for error codes and retry-after headers

## Verification

After generating the integration:
1. Test with a simple GET request (list endpoint)
2. Verify auth works (check response code)
3. Test error handling (invalid ID, missing auth)
4. Check rate limiting (exceed limit, verify backoff)
5. Test pagination (if applicable)
