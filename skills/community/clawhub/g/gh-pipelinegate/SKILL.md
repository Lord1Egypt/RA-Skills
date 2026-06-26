---
name: gh-pipelinegate
description: "Chain Green Helix tools into multi-step pipelines. Define a sequence of steps (scan-text, scan-skill, check-scope, validate, diff, check-env, convert) and PipelineGate executes them in order. Supports stop-on-error or continue-on-failure modes."
metadata: {"openclaw":{"emoji":"⛓️","requires":{"bins":["python"]},"install":[{"id":"pip","kind":"uv","packages":["fastapi","uvicorn","pydantic","pyyaml","jsonschema"]}]}}
---

# PipelineGate

Chain multiple tools into a single pipeline call.

## Start the server

```bash
uvicorn pipelinegate.app:app --port 8011
```

## Run a security pipeline

```bash
curl -s -X POST http://localhost:8011/v1/run \
  -H "Content-Type: application/json" \
  -d '{
    "steps": [
      {"tool": "scan-text", "input": {"text": "Check this text"}},
      {"tool": "scan-skill", "input": {"skill_content": "---\nname: test\n---\nHello"}},
      {"tool": "check-scope", "input": {"skill_content": "---\nname: test\n---\nHello"}}
    ]
  }' | jq
```

Returns `success` (all steps passed), `total_steps`, `completed_steps`, and `results` (output per step).

## Available tools

```bash
curl -s http://localhost:8011/v1/tools | jq '.tools[] | "\(.name): \(.description)"' -r
```

Tools: `scan-text`, `scan-skill`, `check-scope`, `validate`, `diff`, `check-env`, `convert`.

## Error handling

By default, the pipeline stops on the first error. Set `"stop_on_error": false` to continue:

```bash
curl -s -X POST http://localhost:8011/v1/run \
  -H "Content-Type: application/json" \
  -d '{"steps": [{"tool": "scan-text", "input": {"text": "hi"}}], "stop_on_error": false}' | jq
```
