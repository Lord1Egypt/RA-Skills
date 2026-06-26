---
name: datagate
description: "Validate JSON data against a JSON Schema (Draft 2020-12). Post a schema and payload, get back whether it's valid plus detailed error paths and messages for every violation. Language-agnostic validation gate for multi-agent pipelines."
metadata: {"openclaw":{"emoji":"✅","requires":{"bins":["python"]},"install":[{"id":"pip","kind":"uv","packages":["fastapi","uvicorn","pydantic","jsonschema"]}]}}
---

# DataGate

Validate any JSON payload against a JSON Schema.

## Start the server

```bash
uvicorn datagate.app:app --port 8004
```

## Validate data

```bash
curl -s -X POST http://localhost:8004/v1/validate \
  -H "Content-Type: application/json" \
  -d '{
    "json_schema": {
      "type": "object",
      "properties": {"name": {"type": "string"}, "age": {"type": "integer", "minimum": 0}},
      "required": ["name", "age"]
    },
    "payload": {"name": "Alice", "age": 30}
  }' | jq
```

Returns `valid` (true/false), `error_count`, and `errors` (each with `path` pointing to the exact field and `message` explaining the violation).

## Handles invalid schemas too

If you send a broken schema, DataGate catches it and returns an error pointing to `$schema` with a clear message. No crashes.

## Use case

Agents passing data between services can validate payloads before sending. Non-Python agents get Pydantic-grade validation via a simple API call.
