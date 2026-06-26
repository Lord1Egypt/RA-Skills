---
name: gh-agentfinder
description: "Kayak for agents — search across ClawHub, SkillsMP, LobeHub, and more to find the right skill for your task. Compare results across registries, get recommendations for your problem, and discover agents with specific capabilities."
metadata: {"openclaw":{"emoji":"🔎","requires":{"bins":["python"]},"install":[{"id":"pip","kind":"uv","packages":["fastapi","uvicorn","pydantic"]}]}}
---

# AgentFinder

Find the right skill across multiple registries in one call.

## Start the server

```bash
uvicorn agentfinder.app:app --port 8016
```

## Search across all registries

```bash
curl -s -X POST http://localhost:8016/v1/search \
  -H "Content-Type: application/json" \
  -d '{"query": "security scanning"}' | jq
```

Returns results sorted by relevance, from ClawHub, SkillsMP, LobeHub, and more.

## Compare results by registry

```bash
curl -s http://localhost:8016/v1/search/security/compare | jq
```

## Get recommendations for a problem

```bash
curl -s -X POST http://localhost:8016/v1/recommend \
  -H "Content-Type: application/json" \
  -d '{"problem": "I need to validate data before passing it to another agent"}' | jq
```

## Filter by registry

```bash
curl -s -X POST http://localhost:8016/v1/search \
  -H "Content-Type: application/json" \
  -d '{"query": "code review", "registries": ["clawhub"], "max_results": 5}' | jq
```

## List available registries

```bash
curl -s http://localhost:8016/v1/registries | jq
```

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/search | Search across registries |
| GET | /v1/search/{query}/compare | Compare by registry |
| POST | /v1/recommend | Recommend skills for a problem |
| GET | /v1/registries | List available registries |
