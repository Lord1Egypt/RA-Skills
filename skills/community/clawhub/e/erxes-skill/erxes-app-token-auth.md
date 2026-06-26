---
title: erxes Quick Login
description: Minimal login instructions for the erxes skill
---

# erxes Quick Login

Use this when the skill needs to authenticate before a GraphQL call.

## Required input

- `ERXES_BASE_URL`

## Optional input

- `ERXES_CLIENT_ID`
- Default: `erxes-local`

## Login command

```bash
ERXES_BASE_URL=<gateway-url> ERXES_CLIENT_ID=${ERXES_CLIENT_ID:-erxes-local} bash scripts/login.sh
```

Examples:

```bash
ERXES_BASE_URL=https://example.next.erxes.io/gateway bash scripts/login.sh
ERXES_BASE_URL=http://localhost:4000 ERXES_CLIENT_ID=my-client bash scripts/login.sh
```

## What the script does

1. Opens the browser approval page.
2. Waits until the user approves access.
3. Prints session JSON to stdout for the current task.

Do not walk the user through OAuth internals unless they explicitly ask.

## Session payload

The script returns JSON like this:

```json
{
  "subdomain": "demo",
  "base_url": "https://demo.next.erxes.io/gateway",
  "client_id": "erxes-local",
  "token": {
    "tokenType": "Bearer",
    "accessToken": "...",
    "refreshToken": "...",
    "expiresIn": 900
  }
}
```

Use `token.accessToken` for `Authorization: Bearer ...` and `subdomain` for the `erxes-subdomain` header.
Keep this payload in memory for the current task and do not save it to project files.

## When to run it

- Before the first authenticated API call
- Again only if the current session is unavailable or refresh fails
