---
name: cogmate-client
description: Access Cogmate personal knowledge systems via API. Use when querying someone's Cogmate/模拟世界 for knowledge retrieval, semantic search, or Q&A. Requires valid access token from CogNexus (https://github.com/MaxiiWang/CogNexus). Triggers on: "ask Cogmate", "query knowledge base", "search Cogmate", "access 模拟世界".
---

# Cogmate Client

Connect to Cogmate instances for knowledge retrieval and Q&A.

## Prerequisites

- Valid access token (obtain from [CogNexus](https://cognexus.example.com) or instance owner)
- Cogmate API endpoint URL

## Quick Start

### Ask a Question

```bash
curl -X POST "http://{COGMATE_URL}/api/ask?token=YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"question": "你的问题"}'
```

### Semantic Search

```bash
curl "http://{COGMATE_URL}/api/visual/facts?token=YOUR_TOKEN&search=关键词"
```

## API Reference

### Authentication

All protected endpoints require `token` as **query parameter** (not JSON body).

### Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/ask` | POST | Ask questions, get AI-powered answers |
| `/api/visual/facts` | GET | Browse/search knowledge facts |
| `/api/visual/stats` | GET | Get knowledge base statistics |
| `/api/visual/graph` | GET | Get knowledge graph data |
| `/api/hub/profile` | GET | Get Cogmate profile (public) |

### POST /api/ask?token=YOUR_TOKEN

Ask a question against the knowledge base.

**Request:**
```json
{
  "question": "What do you know about X?"
}
```

**Response:**
```json
{
  "answer": "Based on the knowledge base...",
  "sources": [{"id": "fact_xxx", "summary": "..."}]
}
```

### GET /api/visual/facts

Browse or search facts.

**Parameters:**
- `token` (required): Access token
- `search` (optional): Search query
- `layer` (optional): Filter by layer (fact/connection/abstract)

### GET /api/visual/stats

Get statistics about the knowledge base.

**Response:**
```json
{
  "facts": 87,
  "connections": 45,
  "abstracts": 12
}
```

## Token Permissions

| Scope | Capabilities |
|-------|-------------|
| `full` | Complete access: browse, ask, view private |
| `qa_public` | Q&A only (may have usage limits) |
| `browse_public` | Browse public facts only |

## Helper Scripts

### Ask Question

```bash
./scripts/ask.sh <cogmate_url> <token> "Your question"
```

### Search Knowledge

```bash
./scripts/search.sh <cogmate_url> <token> "search term"
```

## Getting Access

1. Visit the Cogmate owner's CogNexus marketplace listing
2. Purchase a token with ATP (platform credits)
3. Use the token to access the Cogmate API

## Error Handling

| Status | Meaning |
|--------|---------|
| 401 | Invalid or expired token |
| 403 | Insufficient permissions |
| 429 | Rate limit exceeded |
| 500 | Server error |

## Example Workflow

```python
import requests

COGMATE_URL = "http://example.com:8000"
TOKEN = "your_token_here"

# Ask a question (token in query params, question in body)
response = requests.post(
    f"{COGMATE_URL}/api/ask",
    params={"token": TOKEN},
    json={"question": "What are the key insights about X?"}
)
print(response.json()["answer"])

# Search facts
facts = requests.get(
    f"{COGMATE_URL}/api/visual/facts",
    params={"token": TOKEN, "search": "keyword"}
).json()
for fact in facts.get("facts", []):
    print(f"- {fact['summary']}")
```
