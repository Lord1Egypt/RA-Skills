---
name: gh-envcheck
description: "Check if your environment is ready to run a skill — verify that required environment variables are set and required CLI binaries are on PATH. Returns a ready/not-ready verdict with lists of present and missing items."
metadata: {"openclaw":{"emoji":"🔧","requires":{"bins":["python"]},"install":[{"id":"pip","kind":"uv","packages":["fastapi","uvicorn","pydantic"]}]}}
---

# EnvCheck

Pre-flight check: does this environment have what the skill needs?

## Start the server

```bash
uvicorn envcheck.app:app --port 8007
```

## Check environment

```bash
curl -s -X POST http://localhost:8007/v1/check-env \
  -H "Content-Type: application/json" \
  -d '{"required_env": ["HOME", "PATH"], "required_bins": ["python", "git"]}' | jq
```

Returns `ready` (true/false), `present_env`, `missing_env`, `present_bins`, `missing_bins`.

## Pair with ScopeCheck

Use ScopeCheck to find out what a skill needs, then EnvCheck to verify your environment has it:

```bash
# Step 1: What does the skill need?
SCOPE=$(curl -s -X POST http://localhost:8002/v1/check-scope \
  -H "Content-Type: application/json" \
  -d "{\"skill_content\": $(cat SKILL.md | jq -Rs)}")

# Step 2: Do we have it?
curl -s -X POST http://localhost:8007/v1/check-env \
  -H "Content-Type: application/json" \
  -d "{\"required_env\": $(echo $SCOPE | jq '.detected.env_vars'), \"required_bins\": $(echo $SCOPE | jq '.detected.cli_tools')}" | jq '.ready'
```
