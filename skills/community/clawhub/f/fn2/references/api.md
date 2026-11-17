# FN2 CLI & API reference

The `fn2` CLI is a thin wrapper over the FN2 public REST API
(`https://fn2.ai/api/v1`). Every request is authenticated with
`Authorization: Bearer $FN2_API_KEY`.

## Environment

| Variable        | Required | Default                     | Notes                                   |
| --------------- | -------- | --------------------------- | --------------------------------------- |
| `FN2_API_KEY`   | yes      | —                           | Your `fn2_...` key                      |
| `FN2_API_BASE`  | no       | `https://fn2.ai/api/v1`     | Override for self-hosted / staging      |

## Commands

| Command | What it does | API call |
| ------- | ------------ | -------- |
| `fn2 research "<q>" [--model M] [--raw]` | Grounded, sourced answer | `POST /chat/incognito` |
| `fn2 models` | List usable models | `GET /models` |
| `fn2 usage` | Plan + token usage | `GET /usage` |
| `fn2 agents list [--status S] [--limit N]` | List your agents | `GET /agents` |
| `fn2 agents get <id>` | One agent's settings | `GET /agents/<id>` |
| `fn2 agents create --prompt P [...]` | Create an agent | `POST /agents` |
| `fn2 agents update <id> [...]` | Edit name/prompt/model/labels | `PATCH /agents/<id>` |
| `fn2 agents pause <id>` / `resume <id>` | Pause / resume | `PATCH /agents/<id>` |
| `fn2 agents run <id>` | Run now (async) | `POST /agents/<id>/run` |
| `fn2 agents delete <id>` | Delete agent + history | `DELETE /agents/<id>` |
| `fn2 runs list <agent-id> [--limit N]` | List an agent's runs | `GET /agents/<id>/runs` |
| `fn2 runs get <agent-id> <run-id>` | A run's outcome + full answer | `GET /agents/<id>/runs/<run-id>` |

Add `--json` (after the command, e.g. `fn2 research "…" --json`) to print the raw
API response. On `research`, `--raw` keeps the platform's inline `{{cite:...}}`
citation markers instead of stripping them for readability.

## Scheduling flags for `agents create`

Pick **one** (omit all for a one-off run that executes immediately):

- `--every <frequency>` — recurring, e.g. `daily`, `weekdays`, `hourly`, `weekly`
- `--cron "<expr>"` — a cron expression, e.g. `"0 9 * * 1"` (Mondays 9am)
- `--at <ISO datetime>` — a single future run, e.g. `2026-07-01T09:00:00`

Optional with any of the above:

- `--timezone <IANA tz>` — e.g. `America/New_York` (default `UTC`)
- `--ends <YYYY-MM-DD>` — stop recurring after this date

## API scopes

API keys carry scopes. The CLI maps to them as follows:

| Scope    | Unlocks                          |
| -------- | -------------------------------- |
| `chat`   | `research`                       |
| `agents` | `agents …`, `runs …`, `usage`    |
| `models` | `models`                         |

A `403 Missing scope` means the key lacks the scope for that command — edit the
key at https://fn2.ai.

## Response shapes

`research` →

```json
{ "response": "<markdown answer>", "status": "success", "request_id": "..." }
```

`agents create` / `get` / `update` →

```json
{
  "id": "…",
  "name": "Macro Brief",
  "recurring": true,
  "schedule": { "frequency": "weekdays", "cron": null, "timezone": "America/New_York",
                "run_at": null, "next_run_at": "…", "ends_at": null },
  "status": "active",
  "run_count": 3,
  "last_run_at": "…",
  "prompt": "…",
  "model": "…",
  "labels": []
}
```

`runs get` →

```json
{
  "run_id": "…",
  "agent_id": "…",
  "status": "completed",
  "duration_seconds": 42.1,
  "usage": { "input_tokens": 1234, "output_tokens": 567, "total_tokens": 1801 },
  "error": null,
  "result": { "text": "<the agent's full answer>" }
}
```

## HTTP status codes

| Code | Meaning |
| ---- | ------- |
| 200 / 201 / 202 | Success |
| 204 | Deleted (no body) |
| 401 | Invalid or inactive API key |
| 403 | API key missing a required scope |
| 404 | Agent or run not found |
| 429 | Quota exceeded — see `fn2 usage` |
