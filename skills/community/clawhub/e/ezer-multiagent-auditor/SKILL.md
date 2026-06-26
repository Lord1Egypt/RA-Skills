---
name: ezer_audit_api
description: Wrapper skill for the Ezer audit backend API. Use this skill when the user asks to run a financial audit task by code/period/year/lang and return structured final audit output from the Ezer API.
metadata:
  {
    "openclaw": {
      "requires": {
        "env": ["EZER_API_BASE_URL"],
        "bins": ["python3"]
      }
    }
  }
---

# Ezer Audit API Skill

This skill wraps the existing Ezer backend API and returns task result payloads.

## When to use

Use this skill when the user wants to run an Ezer audit task with these fields:

- `code` (example: `300750.SZ`)
- `period` (`FY|Q1|Q2|Q3|H1`)
- `year` (integer)
- `lang` (example: `zh-CN`)

## Required environment

- `EZER_API_BASE_URL` example: `http://127.0.0.1:8008`
- `EZER_BEARER_TOKEN` optional if API auth is disabled

## Run command

```bash
python3 {baseDir}/scripts/invoke_ezer_api.py \
  --code 300750.SZ \
  --period FY \
  --year 2021 \
  --lang zh-CN
```

## Behavior

1. POST `/api/tasks` to create task.
2. Poll `/api/tasks/{task_id}/result` until completion or timeout.
3. Print final JSON payload to stdout.

## Notes

- This skill does not expose any model-provider keys.
- If the API returns failure, pass through error payload and non-zero exit.
