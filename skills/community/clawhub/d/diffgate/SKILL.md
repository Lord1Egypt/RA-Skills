---
name: diffgate
description: "Compare two texts and get a unified diff with a similarity score (0-1), line-level additions/deletions, and individual change records. Useful for comparing LLM outputs, verifying content integrity, or tracking document changes."
metadata: {"openclaw":{"emoji":"📊","requires":{"bins":["python"]},"install":[{"id":"pip","kind":"uv","packages":["fastapi","uvicorn","pydantic"]}]}}
---

# DiffGate

Compare two texts and see exactly what changed.

## Start the server

```bash
uvicorn diffgate.app:app --port 8006
```

## Compare texts

```bash
curl -s -X POST http://localhost:8006/v1/diff \
  -H "Content-Type: application/json" \
  -d '{"text_a": "hello\nworld", "text_b": "hello\nearth"}' | jq
```

Returns `similarity` (1.0 = identical, 0.0 = completely different), `additions`, `deletions`, and `changes` (each with `type` add/delete and `content`).

## Use cases

- Compare two LLM outputs to check consistency
- Verify a document hasn't been tampered with
- Track changes between skill versions
- Diff config files before and after an update
