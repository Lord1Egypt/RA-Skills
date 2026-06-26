---
name: garss-studio-rss-api
description: Use when an AI agent needs to read, refresh, summarize, or inspect RSS news from this GARSS Studio project through its backend API. Covers login with access code, Bearer token usage, reader item endpoints, subscription lookup, and the single-port API constraint.
version: 1.0.0
metadata:
  short-description: Read GARSS Studio RSS news through the backend API
  openclaw:
    requires:
      bins:
        - curl
    envVars:
      - name: GARSS_BASE_URL
        required: false
        description: Optional GARSS Studio base URL. Defaults to http://127.0.0.1:25173.
      - name: GARSS_ACCESS_CODE
        required: false
        description: Optional GARSS Studio access code. Defaults to banana for the local dev setup.
---

# GARSS Studio RSS API

Project repository: `https://github.com/zhaoolee/garss`.

Use this skill when the user asks an AI agent to get RSS news from this project, summarize subscribed RSS articles, inspect GARSS Studio subscriptions, refresh a feed, or work with this project's backend API.

## Core Rules

- Use the single public entrypoint only: `http://127.0.0.1:25173` in local dev unless the user gives another base URL.
- Do not access the backend container port or RSSHub container directly.
- If the local service is not running and the user wants live data, start GARSS Studio from the repository before calling APIs.
- Authenticate before calling protected endpoints.
- Prefer cached reads unless the user explicitly asks to refresh.
- Preserve source names and original article links in user-facing summaries.

## Local Startup

Use these steps when the user asks for live GARSS data and `http://127.0.0.1:25173/api/health` is not reachable.

1. Go to the project:

```bash
cd path/to/garss/garss-studio
```

If the repository is not present, clone `https://github.com/zhaoolee/garss` first, then enter `garss-studio`.

2. Ensure env file exists:

```bash
cp .env.example .env
```

Skip this if `.env` already exists.

3. Start the local development stack:

```bash
docker compose -f docker-compose.dev.yml up --build -d
```

Development mode exposes only one public port: `http://127.0.0.1:25173`. The backend and RSSHub services stay behind the frontend gateway. The dev compose defaults `SCHEDULER_ENABLED=false`, so startup should not trigger a full automatic RSS refresh.

4. Verify service health:

```bash
curl -sS http://127.0.0.1:25173/api/health
```

The browser entry is `http://127.0.0.1:25173/reader?pw=banana`.

## Auth Flow

1. Login:

```bash
curl -sS -X POST "$BASE_URL/api/auth/login" \
  -H 'Content-Type: application/json' \
  -d '{"accessCode":"banana"}'
```

2. Read `token` from the JSON response.
3. Call protected endpoints with:

```text
Authorization: Bearer <token>
```

If the user gives a URL containing `?pw=...`, use that value as `accessCode`.

## Reading RSS News

For the user's subscribed RSS news, call:

```bash
curl -sS "$BASE_URL/api/reader/items" \
  -H "Authorization: Bearer $TOKEN"
```

This returns aggregated articles across enabled subscriptions, normally sorted newest first by the backend/frontend contract. Use `?refresh=true` only when the user asks to force refresh, because it will fetch real upstream RSS sources and update cache.

For one source:

1. Call `GET /api/subscriptions` to find the subscription `id`.
2. Call `GET /api/reader/subscriptions/{id}`.
3. Add `?refresh=true` only for a forced refresh.

## Response Handling

Reader items normally include fields such as `title`, `link`, `publishedAt`, `subscriptionId`, `subscriptionName`, author/content fields, and optional HTML. When summarizing:

- Sort by `publishedAt` descending if needed.
- Group by `subscriptionName` when useful.
- Include the original `link`.
- Mention fetch errors from the `errors` array if present.
- Do not expose Bearer tokens in final answers.

## API Reference

For endpoint details, read [references/api.md](references/api.md) only when needed.

The running backend also exposes:

- Swagger UI: `/api/docs`
- OpenAPI JSON: `/api/openapi.json`
