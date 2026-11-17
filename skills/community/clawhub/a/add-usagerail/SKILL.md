---
name: add-usagerail
description: Add API keys, per-customer rate limits, quotas and usage metering to a Node.js or Python API server with the UsageRail SDK. Use when someone wants to sell access to their API, charge by usage through their own Stripe account, or keep one customer from using up their API.
tags: [api, api-keys, rate-limiting, usage-billing, stripe, fastapi, express, django, flask, hono]
---

# Add UsageRail to an API

UsageRail's SDK checks API keys, applies rate limits and quotas, and counts usage per customer inside the user's own API server. Requests never pass through UsageRail. Counts go to UsageRail in the background every 60 seconds.

## Before you change anything

1. Find the framework. The SDKs cover Express, Hono, Fastify and Next.js on Node.js 22+, and FastAPI, Starlette, Flask and Django on Python 3.10+. For other languages, use the HTTP check endpoint described at https://usagerail.com/docs. It adds one network call per request.
2. Ask how callers authenticate today. With no keys yet, use `auth: "api-key"` and UsageRail issues the keys. With existing keys or logins, use `auth: "custom"` with a `consumer` function. In Node.js it returns `{ id }` for the caller, or `null` for anonymous traffic. In Python it returns the customer's ID as a string, or `None`. A bare string returned in Node.js is counted as anonymous. Return an identity the app's own code has verified, never a value the caller can set, such as a plain header. UsageRail has to run after that authentication: in Express, `app.use(usageRail(...))` goes after the auth middleware. In FastAPI the identity must come from an authentication middleware, not `Depends(...)`, and since FastAPI runs the middleware added last first, add the auth middleware after the line that adds UsageRail. In Django, list UsageRail after `AuthenticationMiddleware`. Django REST framework token or JWT authentication runs inside the view, after all middleware, so a consumer that reads `request.user` sees anonymous traffic: verify the token in the consumer function or in an earlier middleware. In Flask, register the app's own `before_request` hook first.
3. The user needs an app key from https://app.usagerail.com. Read it from the `USAGERAIL_APP_KEY` environment variable. Never write the key into source code, and never ask the user to paste it into the chat.

## Wire it in

Every request counts as 1 by default. The `track()` calls below only change that once the app counts units, which is set in the console under Settings > What counts as usage. While the app counts requests, `track()` does nothing.

### FastAPI or Starlette

```bash
pip install usagerail
```

```python
import os

from fastapi import FastAPI, Request
from usagerail.fastapi import UsageRailMiddleware

app = FastAPI()
app.add_middleware(UsageRailMiddleware, app_key=os.environ["USAGERAIL_APP_KEY"], auth="api-key")


@app.post("/v1/generate")
async def generate(request: Request):
    result = await run_model(await request.json())
    request.state.usagerail.track(result.tokens)  # optional: count tokens instead of requests
    return result.body
```

### Flask

```python
import os

from flask import Flask
from usagerail.flask import UsageRail

app = Flask(__name__)
UsageRail(app, app_key=os.environ["USAGERAIL_APP_KEY"], auth="api-key")
```

Inside a route, `g.usagerail.track(n)` counts custom units.

### Django

```python
# settings.py
import os

MIDDLEWARE = [
    # ...
    "usagerail.django.UsageRailMiddleware",
]
USAGERAIL = {"app_key": os.environ["USAGERAIL_APP_KEY"], "auth": "api-key"}
```

Inside a view, `request.usagerail.track(n)` counts custom units.

Under uvicorn or another ASGI server, wrap the application in `asgi.py`, or every restart loses the counts that hadn't gone out yet:

```python
import os

from django.core.asgi import get_asgi_application
from usagerail.django import asgi

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

application = asgi(get_asgi_application())
```

### Express

```bash
npm install @usagerail/node
```

```js
import express from "express";
import { usageRail } from "@usagerail/node/express";

const app = express();

app.use(usageRail({
  appKey: process.env.USAGERAIL_APP_KEY,
  auth: "api-key",
}));

app.post("/v1/generate", express.json(), async (req, res) => {
  const result = await generate(req.body);
  req.usageRail.track(result.tokens); // optional: count tokens
  res.json(result);
});
```

Hono and Fastify have their own entry points: `@usagerail/node/hono` and `@usagerail/node/fastify`. Hono on Node.js doesn't flush on its own: also call `flushOnExit(rail.engine)` from `@usagerail/node/node`, or counts not yet sent are lost when the process stops. Follow the framework's page in the docs for the full setup.

On SIGTERM the Express middleware sends what's left, waiting at most 5 seconds, then lets the process exit. If the app handles SIGTERM itself, keep the value `usageRail()` returned and finish the app's own shutdown with `await middleware.engine.close()`.

## How callers send their key

In the `Authorization: Bearer <key>` header, or in `x-api-key` when there's no bearer token.

## What rejected requests look like

| Status | Meaning |
|---|---|
| 401 | Unknown or revoked key |
| 402 | Prepaid credit used up |
| 403 | Suspended customer |
| 429 | Rate limit or quota reached |
| 503 | UsageRail unreachable, and the app is set to refuse |

Update the API's own docs and client error handling for these.

## Tell the user before they deploy

- Rate limits are counted per server instance by default.
- The Express middleware and the Python SDK don't check or count WebSocket connections. Hono counts a successful handshake once, and so does Fastify with `@fastify/websocket`.
- Counts are sent every 60 seconds. A process killed with `kill -9` or by running out of memory loses the counts it hadn't sent, and they're never billed. A normal shutdown sends them first, with the exceptions above: Django under an ASGI server needs the `asgi.py` wrapper, and Hono needs `flushOnExit`.
- To charge customers, the user connects their own Stripe account. Money goes straight there, and UsageRail is not a merchant of record.

Setup for each framework, options and known limitations: https://usagerail.com/docs
