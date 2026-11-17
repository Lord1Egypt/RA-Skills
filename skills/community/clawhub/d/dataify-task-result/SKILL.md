---
name: dataify-task-result
description: "Download the JSON result of a completed Dataify scraper task. Use when status is successful or the user asks to retrieve results for a known task ID. Do not use merely to check whether a task is still running."
---

# Dataify Task Result

Retrieve one completed task's JSON result from the Dataify `/download` endpoint. Read the API key only from `DATAIFY_API_TOKEN` and never include it in output.

## Workflow

1. Require a task ID. Reuse an unambiguous task ID from the preceding task-status response when its status is `成功`.
2. If the status is unknown, query it first with `$dataify-task-status` unless the user explicitly asks to retrieve the task result directly.
3. Ensure `DATAIFY_API_TOKEN` is set. Do not ask the user to paste an API key into chat or pass one on the command line.
4. Run `scripts/download_task_result.py --task-id TASK_ID`. The script always sends `type=json`.
5. Return the JSON response. If the provider reports an error, return the provider message without retrying the task automatically.

## Commands

```bash
python3 -X utf8 scripts/download_task_result.py --task-id "TASK_ID"
```

To preview the request without downloading the result:

```bash
python3 scripts/download_task_result.py --task-id "TASK_ID" --dry-run
```

## Reference

Read `references/task_result_api.md` for request parameters and response behavior.

## Quick Start

```bash
python3 scripts/download_task_result.py --task-id "TASK_ID" --dry-run
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
