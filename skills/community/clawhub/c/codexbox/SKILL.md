---
name: codexbox
description: "Install, configure, or run Codex through the codexbox wrapper, or connect to its HTTP, MCP, Telegram, or cron surfaces."
homepage: https://github.com/psyb0t/docker-codexbox
user-invocable: true
metadata:
  { "openclaw": { "emoji": "🧑‍💻", "primaryEnv": "CODEXBOX_URL", "requires": { "bins": ["docker", "curl"] } } }
---

# codexbox

[OpenAI Codex CLI](https://github.com/openai/codex) inside an [aicodebox](https://github.com/psyb0t/docker-aicodebox) container, put on the network. codexbox is aicodebox's `codex` adapter. The HTTP/MCP/Telegram/cron surfaces are aicodebox's, the argv/JSON-event translation is codexbox's.

For installation and configuration, see [references/setup.md](references/setup.md).

## Agent execution

Use `codexbox` when it is on `PATH`. Run it from the workspace the user
named. Do not assemble a new `docker run` command for routine interactive or
one-shot work. The wrapper owns the workspace mount, `~/.codex`, SSH state,
image selection, and session lifecycle.

```bash
codexbox                                      # interactive Codex TUI
codexbox exec "inspect this workspace"        # one-shot work
printf '%s\n' "summarize README.md" | codexbox exec -
CODEXBOX_FULL=1 codexbox exec "run the full suite"
```

For a wrapper-started server, prefix container variables with
`CODEXBOX_ENV_`. For example,
`CODEXBOX_ENV_CODEXBOX_API_MODE=1 codexbox` passes
`CODEXBOX_API_MODE=1` into the container. Bare `CODEXBOX_API_MODE` is not
forwarded and does not start the server.

Start a local API and MCP server only when the user asks for one. Authenticate
Codex with `codexbox login --device-auth` or `CODEXBOX_ENV_OPENAI_API_KEY`,
then set the actual model identifiers and distinct bearer tokens:

```bash
CODEXBOX_ENV_CODEXBOX_API_MODE=1 \
CODEXBOX_ENV_CODEXBOX_MCP_MODE=1 \
CODEXBOX_ENV_CODEXBOX_AVAILABLE_MODELS=your-model-id \
CODEXBOX_ENV_CODEXBOX_API_MODE_TOKEN=your-api-token \
CODEXBOX_ENV_CODEXBOX_MCP_MODE_TOKEN=your-mcp-token \
codexbox
```

Use an HTTP or MCP endpoint only when the user asks for a service or provides
an already-running remote URL. MCP plugins connect to a server. They do not
replace the local wrapper.

If `codexbox`, `claudebox`, and `pibox` were installed in the same command
directory, a box can invoke a sibling command directly. The parent wrapper
passes the real host paths and the sibling wrapper file. Do not set
`AICODEBOX_HOST_*`, copy wrapper files, or manually mount another box's state
directory. If the sibling command is absent, ask the user to install it or to
choose another approach.

## Security & safety

- **Set the mode tokens before exposing a port.** `CODEXBOX_API_MODE_TOKEN` (REST) and `CODEXBOX_MCP_MODE_TOKEN` (MCP) each default to no auth when unset, leaving that surface open to anyone who can reach it: run-execution plus full workspace file access. The two are independent (the MCP token has no fallback to the API token), so set whichever mode(s) you enable, and bind to loopback / behind an authenticating proxy. Per-mode detail: [HTTP REST API mode](#http-rest-api-mode), [MCP server mode](#mcp-server-mode).
- **File deletion has no undo.** The run/file tools include a remove operation; only delete files the current task created, only when the user asked, and don't touch another caller's data on a shared workspace.
- **The one-line installer pipes a remote script into `bash`.** Piping a remote script straight into bash executes unreviewed remote code as you. Prefer download → inspect → run (shown in [references/setup.md](references/setup.md)) unless you already trust the source and channel.

## When To Use

- Drive Codex from a script/CI job via `POST /run` instead of a terminal session.
- Point an OpenAI-SDK client at Codex via `/openai/v1/chat/completions` (drop-in base-URL swap).
- Wire Codex into an MCP-aware agent (Claude Code, another OpenClaw agent, Cursor) as a tool-calling backend.
- Run Codex from Telegram on a phone, or on a cron schedule with no human in the loop.
- Manage workspace files (upload/download/list/delete) over HTTP without a shell.

## When NOT To Use

- Need `--append-system-prompt` exact CLI semantics. codex has no such flag; codexbox maps `appendSystemPrompt` to `-c developer_instructions=...` (a developer-role message), not a raw prompt prepend.
- Need per-tool allow/deny lists. codex has no name-based built-in tool allowlist. `toolsAllowlist` is accepted for cross-adapter API compatibility but logged and ignored. `noTools` is the only lever (drops shell/exec + web_search, forces the sandbox read-only).
- Need codex's own MCP client/server support (`[mcp_servers.*]` in `config.toml`, `codex mcp-server` stdio). That's a different, unrelated surface from the MCP mode documented here (which is aicodebox's file-ops + prompt-running MCP surface, not codex's).
- Multiple concurrent runs against the *same* workspace. The API/OAI/MCP surfaces all serialize per-workspace; a second run against a busy workspace gets 409.

## Shell mode

The default. `codexbox` (installed wrapper) or raw `docker run` drop you into `codex`'s interactive TUI, or run codex subcommands directly. No env flag: this is the base behavior with no `*_MODE` var set.

```bash
export OPENAI_API_KEY=sk-...
codexbox                       # interactive TUI, continues the last session for this dir
codexbox --no-continue         # same, but starts a brand-new session
codexbox login --device-auth   # ChatGPT-subscription OAuth login
codexbox stop                  # stop this dir's running container(s)
```

The wrapper mounts `$PWD` as the workspace, persists `~/.codex`, forwards `"$@"` straight to the image, so any `codex` subcommand works (`codexbox mcp ...`, `codexbox doctor`, etc.). The sandbox-bypass flag is injected inside the container automatically.

## One-shot exec mode

`codex exec` (or `codexbox exec` through the wrapper): single prompt in, output to your terminal, no TUI.

```bash
codexbox exec "fix the failing test in ./app"
echo "summarize README.md" | codexbox exec -     # prompt via stdin
```

Raw Docker equivalent:

```bash
docker run --rm \
  -e OPENAI_API_KEY=sk-... \
  -v "$PWD:/workspace" \
  -v "$PWD/.codex:/home/aicode/.codex" \
  psyb0t/codexbox:latest \
  exec "say HELLO"
```

## API mode

`CODEXBOX_API_MODE=1`. FastAPI server on `:8080` (override `CODEXBOX_API_MODE_PORT`). **Requires** `CODEXBOX_AVAILABLE_MODELS=<csv>`. API mode refuses to boot without it (codex has no hardcoded model slug to fall back to).

```bash
docker run -d --name codexbox-api \
  -e CODEXBOX_API_MODE=1 \
  -e CODEXBOX_API_MODE_TOKEN=your-secret \
  -e CODEXBOX_AVAILABLE_MODELS=gpt-5.1-codex,gpt-5.1-codex-mini \
  -e OPENAI_API_KEY=sk-... \
  -v "$PWD:/workspace" \
  -p 8080:8080 \
  psyb0t/codexbox:latest
```

With `CODEXBOX_API_MODE_TOKEN` unset the API surface is unauthenticated: anyone who can reach `:8080` gets run-execution plus full workspace file access. Set the token and bind to loopback / behind an authenticating proxy before exposing it beyond localhost.

| Method | Path | What it does |
|--------|------|---------------|
| `GET` | `/healthz` | liveness, `{ok, adapter}`, no token needed |
| `GET` | `/status` | in-flight runs + busy workspaces |
| `POST` | `/run` | sync agent run → `{runId, workspace, exitCode, text, ...}` |
| `GET` | `/run/result?runId=<id>` | poll an async run |
| `DELETE` | `/run/{run_id}` | cancel an in-flight run |
| `GET` | `/files` | list the workspace root |
| `GET` | `/files/{path}` | list a sub-directory, or stream a file's bytes |
| `PUT` | `/files/{path}` | upload: raw request body becomes the file contents; parent dirs auto-created |
| `DELETE` | `/files/{path}` | delete a file (refuses directories with 400) |
| `POST` | `/openai/v1/chat/completions` | OpenAI-compatible chat endpoint (see below) |
| `GET` | `/openai/v1/models` | model list from `CODEXBOX_AVAILABLE_MODELS` |
| `POST` | `/mcp/` | MCP server, mounted only when `CODEXBOX_MCP_MODE=1` (see MCP mode) |

`DELETE /files/{path}` removes a workspace file (no undo). Confirm the target path first and only remove files the current task created. See [Security & safety](#security--safety).

`POST /run` body: `prompt` (required), `workspace`, `model`, `systemPrompt`, `appendSystemPrompt`, `jsonSchema`, `eventMode`, `outputFormat`, `noContinue`, `resume`, `timeoutSeconds`, `thinking`, `noTools`, `toolsAllowlist`, `includeRaw`, `async`, `fireAndForget`. With `jsonSchema` set, the response adds `json`, `events`, `sessionId`, `usage`, `attempts`. codex has native `--output-schema` enforcement, so `jsonSchema` maps straight onto it; the shared validator and its retry stay only as a fallback. `"eventMode": "full"` returns every native Codex event, `"none"` only the final result, and the default `"auto"` turns events on for `jsonSchema` requests.

Default programmatic runs continue the exact top-level Codex `exec` root
pinned to the canonical workspace. The first run creates the pin; existing
workspaces migrate their newest top-level `exec` rollout. Newer subagent
rollouts are deliberately excluded because Codex rejects direct turns on
multi-agent children. Explicit `resume` re-pins the confirmed thread;
`noContinue` is ephemeral and leaves the workspace pin unchanged.

```bash
curl -s http://localhost:8080/run \
  --oauth2-bearer "$CODEXBOX_API_MODE_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "say HELLO", "workspace": "/workspace"}'
```

Async: set `"async": true`, poll `GET /run/result?runId=<id>` until `status != "running"`.

All `/files/*` paths are resolved against the workspace root with traversal checking: `..` segments that escape the root return 400.

```bash
curl -sS -X PUT --oauth2-bearer "$CODEXBOX_API_MODE_TOKEN" \
  --data-binary @local.txt http://localhost:8080/files/notes/hello.txt

curl -sS --oauth2-bearer "$CODEXBOX_API_MODE_TOKEN" \
  http://localhost:8080/files/notes/hello.txt
```

## OpenAI-compatible endpoint

`POST /openai/v1/chat/completions` (mounted under API mode, same port/token). Point any OpenAI SDK's base URL at `http://host:8080/openai/v1` and call it like the real API.

- **Streaming**: `"stream": true` gives real incremental SSE for plain chat. When `tools`/`tool_choice` or a schema constraint is also set, the full answer is computed first, then replayed as a single-shot SSE stream (tool-call/schema turns can't be streamed token-by-token).
- **Tools**: OpenAI-style `tools` / `tool_choice` in the request body. codex runs its own tools internally, so client-executed tool calling is bridged: codexbox injects an "emit `{"tool_calls":[...]}` and stop" protocol into the system prompt and parses codex's textual output back into OpenAI `tool_calls`. Stateless: resend full history each round-trip, same as the standard OpenAI tool loop.
- **`response_format`**: `{"type":"text"}` (default), `{"type":"json_object"}` (force parseable JSON, no schema), or `{"type":"json_schema","json_schema":{"name","schema","strict?"}}` (schema-constrained, same native `--output-schema` path as `/run`'s `jsonSchema`). Composable with `tools`: a tool-call turn isn't schema-checked, only the final non-tool answer is.
- Custom headers (`x-aicodebox-*` prefix, `x-claude-*` accepted as aliases for workspace/continue/append-system-prompt) cover what the OpenAI wire format has no field for: `x-aicodebox-workspace`, `x-aicodebox-continue`, `x-aicodebox-resume`, `x-aicodebox-json-schema` (fallback if `response_format` isn't set), `x-aicodebox-no-tools`, `x-aicodebox-tools-allowlist`, `x-aicodebox-timeout-seconds`, `x-aicodebox-extra-args`.

```bash
curl -s http://localhost:8080/openai/v1/chat/completions \
  --oauth2-bearer "$CODEXBOX_API_MODE_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
        "model": "gpt-5.1-codex",
        "messages": [{"role": "user", "content": "say HELLO"}],
        "stream": false
      }'
```

## MCP mode

`CODEXBOX_MCP_MODE=1`. Exposes the aicodebox base's own MCP surface, file ops + prompt running as tools: `run_prompt`, `list_files`, `read_file`, `write_file`, `delete_file`. This is separate from codex's own MCP client/server support (`config.toml` `[mcp_servers.*]`, `codex mcp-server` stdio). codexbox wires up neither of those.

Coexists with any foreground mode:

| Foreground | MCP placement |
|---|---|
| API mode (`CODEXBOX_API_MODE=1`) | mounted at `/mcp/` on the API port, no extra process |
| Telegram / Cron / shell-only | sidecar uvicorn on `CODEXBOX_MCP_MODE_PORT` (default `8081`), served at the process root |

The slashless `/mcp` spelling reaches the same API-mounted handler without a redirect. The `@psyb0t/codexbox` stdio bridge appends `CODEXBOX_MCP_PATH` (default `/mcp/`) to `CODEXBOX_URL`; set `CODEXBOX_MCP_PATH=/` to reach the sidecar.

Auth: `CODEXBOX_MCP_MODE_TOKEN=<token>`: bearer in `Authorization: Bearer ...`, or `?apiToken=...` for clients that can't set headers. Empty = no auth. **No fallback to `API_MODE_TOKEN`**: MCP has its own bearer, checked independently.

With `CODEXBOX_MCP_MODE_TOKEN` unset the MCP surface (`run_prompt`, `list_files`, `read_file`, `write_file`, `delete_file`) is unauthenticated: anyone who can reach `/mcp/` or the sidecar port gets run-execution plus full workspace file access. This surface has its own bearer; setting `CODEXBOX_API_MODE_TOKEN` does not protect it. Set the token and bind to loopback / behind an authenticating proxy before exposing it beyond localhost.

MCP keeps DNS rebinding protection enabled. Loopback hosts and origins work by default; allow a reverse proxy's exact `Host` and browser `Origin` with `CODEXBOX_MCP_MODE_ALLOWED_HOSTS` and `CODEXBOX_MCP_MODE_ALLOWED_ORIGINS` before exposing MCP through it.

```bash
docker run -d --name codexbox-api \
  -e CODEXBOX_API_MODE=1 -e CODEXBOX_API_MODE_TOKEN=your-secret \
  -e CODEXBOX_MCP_MODE=1 -e CODEXBOX_MCP_MODE_TOKEN=your-mcp-secret \
  -e CODEXBOX_AVAILABLE_MODELS=gpt-5.1-codex \
  -e OPENAI_API_KEY=sk-... \
  -v "$PWD:/workspace" -p 8080:8080 \
  psyb0t/codexbox:latest
```

Wire into an MCP-aware client:

```bash
claude mcp add --transport http codexbox http://localhost:8080/mcp/ \
  --header "Authorization: Bearer your-mcp-secret"
```

## Telegram mode

`CODEXBOX_TELEGRAM_MODE=1` + `CODEXBOX_TELEGRAM_MODE_TOKEN=<token-from-BotFather>`.

```bash
docker run -d --name codexbox-tg \
  -e CODEXBOX_TELEGRAM_MODE=1 \
  -e CODEXBOX_TELEGRAM_MODE_TOKEN=123456:ABC-your-bot-token \
  -e OPENAI_API_KEY=sk-... \
  -v "$PWD:/workspace" \
  -v "$HOME/.aicodebox:/home/aicode/.aicodebox" \
  psyb0t/codexbox:latest
```

- Text in → codex runs → Markdown→HTML rendered response back.
- File uploads land in the chat's workspace. `[SEND_FILE: path]` in codex's output delivers workspace files as Telegram attachments.
- Per-chat overrides: `/model`, `/effort` (codex's `model_reasoning_effort` levels), `/system_prompt`, `/append_system_prompt`. Persisted to `CODEXBOX_TELEGRAM_MODE_OVERRIDES`.
- `/cancel` kills the in-flight run, `/reload` re-reads config, `/config` dumps merged settings, `/fetch <path>` downloads a file.

Access control + per-chat config lives in a YAML file (`CODEXBOX_TELEGRAM_MODE_CONFIG`, default `~/.aicodebox/telegram.yml`):

```yaml
allowed_chats: [-100123, 42]
default:
  model: gpt-5.1-codex
  workspace: shared
chats:
  -100123:
    workspace: alpha
    allowed_users: [10, 20]
```

## Cron mode

`CODEXBOX_CRON_MODE=1` + `CODEXBOX_CRON_MODE_FILE=/path/to/cron.yaml`. 6-field cron schedules via croniter. Each job fires codex non-interactively with the given instruction. Runs together with Telegram mode (cron in-thread inside the telegram process) when both are enabled; otherwise it's its own foreground process.

Via the `codexbox` wrapper (host-side trigger vars, translated into the container-side `CODEXBOX_CRON_MODE*` vars automatically):

```bash
CODEXBOX_MODE_CRON=1 CODEXBOX_MODE_CRON_FILE=/path/cron.yaml codexbox
```

Raw Docker:

```bash
docker run -d --name codexbox-cron \
  -e CODEXBOX_CRON_MODE=1 \
  -e CODEXBOX_CRON_MODE_FILE=/cron/jobs.yaml \
  -e OPENAI_API_KEY=sk-... \
  -v "$PWD/cron.yaml:/cron/jobs.yaml:ro" \
  -v "$PWD:/workspace" \
  psyb0t/codexbox:latest
```

```yaml
jobs:
  - name: morning-standup
    schedule: "0 0 9 * * 1-5"
    instruction: |
      Summarize what changed in /workspace since yesterday.
      Be brief. One paragraph max.
    workspace: myproject
    telegram_chat_id: -100123
    model: gpt-5.1-codex
    thinking: low
```

`CODEXBOX_CRON_MODE_HISTORY_DIR` (default `$HOME/.aicodebox/cron`) is the whole cron state root. Each run gets a history dir at `<root>/history/<workspace>/<timestamp>-<job>/` with `meta.json`, `stdout.log`, `stderr.log`, `result.txt` (plus `telegram.json` when telegram is also configured, and the next run's prompt gets a "prior run" hint automatically). A per-job summary jsonl lands at `<root>/<job>.jsonl`. Set a job's `telegram_chat_id` to `0` to opt it out of an inherited root-level notification target; a successful job with an explicit `telegram_chat_id` still posts a notice even when its result text is empty.

## Auth

Two independent auth layers:

**1. Surface auth** (who can call the HTTP/MCP endpoints): `CODEXBOX_API_MODE_TOKEN` gates `/run`, `/files/*`, `/openai/v1/*`; `CODEXBOX_MCP_MODE_TOKEN` gates `/mcp/` (its own bearer, no fallback to the API token). Empty = no auth on that surface.

**2. codex's own upstream auth** (how codex talks to OpenAI). Pick one:
  - `OPENAI_API_KEY`: seeded into `$CODEX_HOME/auth.json` when a container first starts; safe to always set (never overwrites an existing ChatGPT-subscription login).
  - ChatGPT subscription: one-time `codexbox login --device-auth` with `~/.codex` bind-mounted so the OAuth login survives container recreation. Bills against Plus/Pro/Team instead of API usage; the `*-codex`/`*-codex-mini` model slugs are rejected on a subscription account (400); use the `gpt-5.6-*` family instead.

## Typical Workflows

**Fire a one-off prompt from a script:**

```bash
curl -s http://localhost:8080/run \
  -H "Authorization: Bearer $CODEXBOX_TOKEN" -H "Content-Type: application/json" \
  -d '{"prompt": "list every TODO in /workspace", "workspace": "/workspace"}' | jq -r .text
```

**Drop-in OpenAI SDK swap:**

```python
from openai import OpenAI
client = OpenAI(base_url="http://localhost:8080/openai/v1", api_key="your-secret")
resp = client.chat.completions.create(
    model="gpt-5.1-codex",
    messages=[{"role": "user", "content": "say HELLO"}],
)
print(resp.choices[0].message.content)
```

**Schema-constrained extraction:**

```bash
curl -s http://localhost:8080/run \
  -H "Authorization: Bearer $CODEXBOX_TOKEN" -H "Content-Type: application/json" \
  -d '{
        "prompt": "extract the version + license from README.md",
        "workspace": "/workspace",
        "jsonSchema": {"type": "object", "properties": {"version": {"type": "string"}, "license": {"type": "string"}}, "required": ["version", "license"]}
      }' | jq .json
```

**Async run + poll:**

```bash
run_id=$(curl -s http://localhost:8080/run -H "Authorization: Bearer $CODEXBOX_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "run the full test suite and summarize failures", "async": true}' | jq -r .runId)

curl -s "http://localhost:8080/run/result?runId=$run_id" -H "Authorization: Bearer $CODEXBOX_TOKEN" | jq
```

**Cancel a stuck run:**

```bash
curl -s -X DELETE "http://localhost:8080/run/$run_id" -H "Authorization: Bearer $CODEXBOX_TOKEN"
```
