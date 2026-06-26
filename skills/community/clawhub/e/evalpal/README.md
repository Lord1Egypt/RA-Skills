# EvalPal — ClawHub Skill

Run AI agent evaluations directly from your OpenClaw agent via `/evalpal` slash
commands. Trigger eval runs, check results, and list available evaluations — all
inline in Slack or Discord.

## Installation

```bash
openclaw skills install evalpal
```

## Setup

1. **Get an API key** from [evalpal.dev](https://evalpal.dev) → Settings → API
   Keys.
2. **Add the key** to your OpenClaw skill configuration:

```yaml
# In your OpenClaw agent config
skills:
  entries:
    evalpal:
      env:
        EVALPAL_API_KEY: 'sk_your_key_here'
```

## Commands

### Run an evaluation

```bash
/evalpal run --eval-id <ID>
```

Triggers a full evaluation run. The skill polls for completion (up to 5 minutes)
and prints a formatted summary with pass/fail status per test case.

**Example output:**

```
✅ Evaluation — PASSED (15/16)
├── Test Case tc_001: ✓ PASS
├── Test Case tc_002: ✓ PASS
├── Test Case tc_003: ✗ FAIL
└── 12 more passed...

Run ID: run_abc123 · 16 test cases · 47s
```

### Check run status

```bash
/evalpal status --run-id <ID>
```

Returns the current status of an in-progress or completed run.

### List evaluations

```bash
/evalpal list [--project-id <ID>]
```

Lists all evaluation definitions. Omit `--project-id` to see evals across all
projects.

## Requirements

- `curl` and `jq` must be available (standard on macOS and Linux)
- An EvalPal account with at least one evaluation definition configured

## Troubleshooting

| Problem                       | Fix                                                  |
| ----------------------------- | ---------------------------------------------------- |
| `EVALPAL_API_KEY is not set`  | Add your API key to the OpenClaw skill env config    |
| `Authentication failed (401)` | Verify your API key is valid and hasn't been revoked |
| `Eval definition not found`   | Run `/evalpal list` to find valid eval IDs           |
| `Rate limited (429)`          | Wait and retry; reduce eval frequency if persistent  |
| `Could not reach EvalPal API` | Check network connectivity and `EVALPAL_API_URL`     |

## Links

- [EvalPal](https://evalpal.dev) — AI evaluation platform
- [EvalPal Docs](https://evalpal.dev/api/docs) — API documentation
- [OpenClaw](https://openclaw.ai) — AI agent platform
- [ClawHub](https://clawhub.ai) — Skill marketplace
