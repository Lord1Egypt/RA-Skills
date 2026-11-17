---
name: dataify-task-operations
description: "Monitor a Dataify Builder task through completion, recover safely after interruption, or guide cross-platform DATAIFY_API_TOKEN setup. Use automatically after scraper submission, when the user provides an existing task ID, or asks how to configure the token. Do not use when the user explicitly requests submission-only behavior."
---

# Dataify Task Operations

Complete the asynchronous task lifecycle instead of stopping at task creation. The default product result is the collected data, not the task ID.

## Contract

Treat task states as `submitted`, `queued`, `running`, `succeeded`, `failed`, or `cancelled`. Preserve an unknown provider state verbatim and map it only when the meaning is unambiguous.

## Workflow

1. Require a task ID. Reuse one returned earlier in the conversation when unambiguous.
2. Read `DATAIFY_API_TOKEN` from the environment. Never accept or print it as a command-line argument. If it is missing, follow [Token setup](references/token-setup.md), show only the current platform's setup command, and resume this workflow after safe verification.
3. Use an installed Dataify task-status/result tool when available. Do not invent an endpoint that is not documented in the repository or exposed by a connected tool.
4. After a scraper submission, monitor by default with `scripts/wait_for_task.py`. Stop at submission only when the user explicitly asks for a task ID or `--no-wait` behavior.
5. If status is queued or running, continue bounded monitoring. Do not ask the user to request monitoring separately.
6. If succeeded, download and return the available result. Summarize large results and preserve access to raw data.
7. If failed, return the provider error, likely corrective action, and whether retrying is safe.
8. If monitoring times out or is interrupted, report the task ID and exact resume command. Never resubmit merely because monitoring stopped.
9. If no status/result capability is installed, report the task ID and dashboard URL as an explicit handoff. State that automated retrieval is unavailable; do not claim completion.

## Deterministic monitor

```bash
python3 scripts/wait_for_task.py --task-id TASK_ID
```

The script polls `GET /task_status`, maps `处理中` to running, downloads JSON from `GET /download` after `成功`, stops on `失败`, and never resubmits the original paid task.

## Wait profiles

- Default: wait up to 600 seconds with a maximum 15-second polling interval.
- Media downloads and clearly high-volume or multi-page collections: use `--timeout 1800`.
- A timeout stops only local monitoring. The remote task continues and must be resumed with the same task ID.
- Use a custom timeout only when the task's expected size justifies it; never use an unbounded loop.

## Safety

- Do not retry paid or high-volume tasks without confirmation.
- Do not expose tokens, cookies, signed URLs, or private result contents in logs.
- Do not infer success from the presence of a task ID.

## Token helper

Use the cross-platform helper when environment detection or non-secret verification is useful:

```bash
python3 scripts/token_setup.py
```

It reports whether the variable exists and prints the matching setup/verification commands when missing. It never prints the token value.

## Quick Start

```bash
python3 scripts/wait_for_task.py --task-id TASK_ID
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
- For a missing token, offer https://dashboard.dataify.com/login?utm_source=skill and state: New accounts get 50 free credits, enough for about 6,000 trial results, valid for 7 days, and only successful requests are billed. Never ask the user to paste the token into chat.
- Detect the current operating system and shell. Show only the matching session-scoped setup command first (`export` for macOS/Linux shells, `$env:` for Windows PowerShell, or `set` for Windows Command Prompt). Show other platforms or persistent setup only when detection is ambiguous or the user asks.
- After the user says the token is configured, verify only whether `DATAIFY_API_TOKEN` is present; never print its value. If verification succeeds, continue the original task without asking the user to repeat it.
- Explain that persistent shell changes may require a new terminal or restarting the agent application. Do not recommend a project `.env` unless the execution path explicitly loads it, and ensure `.env` is ignored by version control.
- For an invalid token, direct the user to API-key management without implying that a new registration is required. For insufficient credits, direct the user to balance or recharge management.
- During normal submission, processing, and successful completion, do not promote registration or the Dashboard. Never expose the token or include it in CTA attribution parameters.
