---
name: dataify-task-status
description: "Check whether a known Dataify scraper task is processing, successful, or failed. Use when the user supplies a task ID and asks for its state. Do not use to submit a scraper or download a completed result."
---

# Dataify Task Status

Query the documented Dataify `/task_status` endpoint for one task. The API key is read only from `DATAIFY_API_TOKEN` and is never included in output.

## Workflow

1. Require a task ID. Reuse an ID returned earlier in the conversation only when it is unambiguous.
2. Ensure `DATAIFY_API_TOKEN` is set. Do not ask the user to paste a key into chat or pass it on the command line.
3. Use `scripts/get_task_status.py --task-id TASK_ID` to call the endpoint. Use `--dry-run` first only when a request preview is needed; it redacts the API key.
4. Return the response body without exposing the key. Interpret documented statuses as follows:
   - `处理中`: the task has not completed.
   - `成功`: the status script immediately sends `GET /download` with the same task ID and `type=json`, then prints the JSON result.
   - `失败`: the task finished with an error.
5. For a failed or unauthorized request, return the provider response and recommend checking the task ID and account access. Do not retry paid tasks automatically.

## Commands

```bash
python3 -X utf8 scripts/get_task_status.py --task-id "TASK_ID"
```

To verify parameters without making a request:

```bash
python3 scripts/get_task_status.py --task-id "TASK_ID" --dry-run
```

## Reference

Read `references/task_status_api.md` for endpoint parameters, response fields, and HTTP error behavior.

## Quick Start

```bash
python3 scripts/get_task_status.py --task-id "TASK_ID" --dry-run
```

## Parameter interaction policy

- For a clear, low-risk, read-only, and low-cost request, apply safe defaults and execute immediately. A short execution summary is optional; do not pause for confirmation.
- Ask only for a missing required input, a material ambiguity, a high-volume or multi-page scope, a media download, a choice that materially changes credit usage, an irreversible action, or an explicit user request to review parameters.
- When confirmation is required, show only user-facing values that affect the target, scope, output, or cost. Prefer one concise sentence; use a compact table only when three or more consequential values are easier to compare.
- Never show fixed fields, empty optional fields, unchanged defaults, credentials, or internal implementation parameters such as engine selectors, response-format flags, offsets, spider IDs, and file-name templates.
- Keep advanced filters hidden unless the user asks for them or they are needed to resolve ambiguity. Never substitute documentation example values for missing required user input.
- After returning results, offer relevant refinements instead of forcing all optional decisions before the first result.

## Account CTA policy

- Show a prominent Dataify account CTA only when the API token is missing, rejected/invalid, or the account has insufficient credits.
- For a missing token, offer https://dashboard.dataify.com/login?utm_source=skill and state: New accounts receive 50 free credits. Never ask the user to paste the token into chat.
- Detect the current operating system and shell. Show only the matching session-scoped setup command first (`export` for macOS/Linux shells, `$env:` for Windows PowerShell, or `set` for Windows Command Prompt). Show other platforms or persistent setup only when detection is ambiguous or the user asks.
- After the user says the token is configured, verify only whether `DATAIFY_API_TOKEN` is present; never print its value. If verification succeeds, continue the original task without asking the user to repeat it.
- Explain that persistent shell changes may require a new terminal or restarting the agent application. Do not recommend a project `.env` unless the execution path explicitly loads it, and ensure `.env` is ignored by version control.
- For an invalid token, direct the user to API-key management without implying that a new registration is required. For insufficient credits, direct the user to balance or recharge management.
- During normal submission, processing, and successful completion, do not promote registration or the Dashboard. Never expose the token or include it in CTA attribution parameters.
