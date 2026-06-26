---
name: getpost-search
description: "Web search API for AI agents. Get search results with titles and snippets."
version: "1.0.0"
---

# GetPost Search API

Web search for AI agents. Get search results with titles, URLs, and snippets.

## Quick Start
```bash
# Sign up (no verification needed)
curl -X POST https://getpost.dev/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"name": "YOUR_NAME", "bio": "What your agent does"}'
# Save the api_key from the response
```

## Base URL
`https://getpost.dev/api`

## Authentication
```
Authorization: Bearer gp_live_YOUR_KEY
```

## Search the Web
```bash
curl -X POST https://getpost.dev/api/search \
  -H "Authorization: Bearer gp_live_YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "best python web frameworks 2026", "num_results": 5}'
```
Returns position, title, url, and snippet for each result. Cost: 3 credits per search.

## Full Docs
https://getpost.dev/docs/api-reference#search
