---
name: evalpal
description:
  Run AI agent evaluations via EvalPal — trigger eval runs, check results, and
  list available evaluations
homepage: https://evalpal.dev
user-invocable: true
requires:
  env:
    - EVALPAL_API_KEY
  bins:
    - curl
    - jq
---

# EvalPal Skill

Run AI agent evaluations inline. Trigger eval runs, poll for results, and list
available evaluation definitions — all from chat.

## Prerequisites

Set the following environment variables in your OpenClaw skill configuration:

| Variable          | Required | Description                                  |
| ----------------- | -------- | -------------------------------------------- |
| `EVALPAL_API_KEY` | Yes      | Your EvalPal API key (starts with `sk_`)     |
| `EVALPAL_API_URL` | No       | Base URL (defaults to `https://evalpal.dev`) |

Get your API key from **Settings → API Keys** at
[evalpal.dev](https://evalpal.dev).

## Commands

### `/evalpal run --eval-id <ID>`

Trigger an evaluation run and wait for results.

**Usage:**

```bash
bash scripts/run-eval.sh --eval-id <EVAL_DEFINITION_ID>
```

**What it does:**

1. Triggers a new eval run via the EvalPal API
2. Polls for completion with exponential backoff (up to 5 minutes)
3. Fetches and formats results as readable markdown

**Example output:**

```
✅ Episode Quality — PASSED (15/16)
├── Test Case tc_001: ✓ PASS
├── Test Case tc_002: ✓ PASS
├── Test Case tc_003: ✗ FAIL
└── 12 more passed...

Run ID: run_abc123 · 16 test cases · 47s
```

**Exit codes:** 0 = all passed, 1 = failures or error.

### `/evalpal status --run-id <ID>`

Check the current status of a running evaluation.

**Usage:**

```bash
bash scripts/check-status.sh --run-id <RUN_ID>
```

**Example output:**

```
📊 Run Status: run_abc123
Status: running
Started: 2026-03-26T20:00:00Z
```

### `/evalpal list`

List available evaluation definitions across your projects.

**Usage:**

```bash
bash scripts/list-evals.sh [--project-id <PROJECT_ID>]
```

If `--project-id` is omitted, lists evals for all projects.

**Example output:**

```
📋 Evaluation Definitions

Project: AI Workforce Lab
  abc123  Episode Quality Check
  def456  Factual Accuracy Eval

Project: Customer Support Bot
  ghi789  Response Quality
```

## Error Handling

All scripts handle common error cases:

| Scenario        | Output                                       | Exit Code |
| --------------- | -------------------------------------------- | --------- |
| No API key set  | `Error: EVALPAL_API_KEY is not set`          | 1         |
| Invalid API key | `Error: Authentication failed (401)`         | 1         |
| Eval not found  | `Error: Eval definition not found (404)`     | 1         |
| Rate limited    | `Error: Rate limited — retry after Xs (429)` | 1         |
| Timeout (5 min) | `Error: Evaluation timed out after 300s`     | 1         |
| Network error   | `Error: Could not reach EvalPal API`         | 1         |

## Security

- The API key is read from `EVALPAL_API_KEY` environment variable only
- Scripts never echo or log the API key
- All API calls use HTTPS
