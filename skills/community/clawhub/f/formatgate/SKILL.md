---
name: formatgate
description: "Convert between JSON, YAML, and TOML formats. All 6 conversion directions supported. Round-trip safe. Useful for agents that receive data in one format and need it in another."
metadata: {"openclaw":{"emoji":"🔄","requires":{"bins":["python"]},"install":[{"id":"pip","kind":"uv","packages":["fastapi","uvicorn","pydantic","pyyaml"]}]}}
---

# FormatGate

Convert data between JSON, YAML, and TOML.

## Start the server

```bash
uvicorn formatgate.app:app --port 8008
```

## Convert JSON to YAML

```bash
curl -s -X POST http://localhost:8008/v1/convert \
  -H "Content-Type: application/json" \
  -d '{"content": "{\"name\": \"Alice\", \"age\": 30}", "input_format": "json", "output_format": "yaml"}' | jq -r '.result'
```

## Convert YAML to JSON

```bash
echo "name: Alice" | curl -s -X POST http://localhost:8008/v1/convert \
  -H "Content-Type: application/json" \
  -d "{\"content\": $(cat - | jq -Rs), \"input_format\": \"yaml\", \"output_format\": \"json\"}" | jq -r '.result'
```

Returns `success` (true/false), `result` (converted content), and `error` (if conversion failed — e.g., invalid input).
