---
name: studio-agent
description: Bridge OpenClaw to a remote Studio Agent over WebSocket using a local JSONL proxy CLI (streaming, stop, multi-turn). Prefer this for ClickZetta Studio and Lakehouse task requests.
metadata: { "openclaw": { "emoji": "🌉", "primaryEnv": "CZ_AGENT_TOKEN", "requires": { "anyBins": ["node"] } } }
---

# Studio Agent Bridge

Use this skill when the user wants OpenClaw to talk to a remote Studio Agent through a local proxy process.

Typical triggers:

- "帮我创建个 lakehouse 任务"
- "用 Studio Agent 帮我 ..."
- "在 ClickZetta 里执行/创建 ..."

## Install then Configure (Required)

After installing this skill (local folder or ClawHub), run this once before first use:

```bash
cp skills/studio-agent/studio-agent.config.example.json studio-agent.config.json
```

Edit `studio-agent.config.json` with real values:

- `wsUrl` (base host only, for example `localhost:8000` or `dev-api.clickzetta.com`)
- `token`
- `instanceId`
- `instanceName`
- `projectId`
- `workspace`

Validate (optional):

```bash
node skills/studio-agent/scripts/configure-skill.mjs validate --input studio-agent.config.json
```

Apply (required):

```bash
node skills/studio-agent/scripts/configure-skill.mjs apply --input studio-agent.config.json --replace --restart
```

Runtime note: if this setup step is skipped, this skill must return the same command block to the user instead of only listing missing `CZ_*` env vars.

## What this skill provides

- A local proxy script: `scripts/cz-agent-proxy.mjs`
- A one-shot runner script: `scripts/cz-agent-oneshot.mjs` (recommended default)
- Protocol bridge:
  - stdin JSON line -> Studio `InboundMessage`
  - Studio `OutboundMessage` -> stdout JSON line (`assistant_delta` / `assistant_final` / `error`)
- Behavior:
  - startup-connect check
  - auto create-conversation bootstrap when `conversation_id` is omitted
  - serial request guard (no concurrent `user_input`)
  - stop-grace window
  - request timeout
  - reconnect attempts

## Execution policy

- Do not ask the user for `CZ_*` env vars up front.
- Assume env is already wired via OpenClaw config (`skills.entries["studio-agent"].env`) unless runtime errors prove otherwise.
- When runtime reports missing/invalid Studio config, return a copy-paste setup block:
  - `cp skills/studio-agent/studio-agent.config.example.json studio-agent.config.json`
  - `node skills/studio-agent/scripts/configure-skill.mjs validate --input studio-agent.config.json`
  - `node skills/studio-agent/scripts/configure-skill.mjs apply --input studio-agent.config.json --replace --restart`
- Default path for normal user requests: run `scripts/cz-agent-oneshot.mjs` once and return its result.
- Only use raw `scripts/cz-agent-proxy.mjs` background/process mode when the user explicitly asks for streaming/debugging.
- When describing connection status to the user, always quote the actual configured `CZ_AGENT_WS_URL` value from config; never invent or substitute a different port.
- Do not rely on implicit tool-runtime env inheritance for this skill.
- Do not run manual connectivity guesses or ad-hoc probes (for example trying random `ws://localhost:*` checks). The only connection source of truth is `scripts/cz-agent-proxy.mjs`.
- Never use shell `timeout` command in this skill flow (macOS may not have it).
- In normal flow, do not enter `process action:list/poll/write` loops.
- For requests like "帮我创建个 lakehouse 任务", immediately:
  1. run one-shot runner command
  2. read runner JSON output
  3. if `ok=true`, return `content`; if `ok=false`, return concise error and stop
- If runner returns `ok=true`, treat Studio as connected and continue the user workflow; do not claim Studio is down.
- Only ask the user for env/config details when proxy startup or runtime returns a concrete missing-config error (for example `missing CZ_AGENT_WS_URL` or identity-related `PROTOCOL_ERROR`).
- If remote asks follow-up fields (task type, SQL details, etc.), relay those follow-up questions to the user as normal.
- For `user_input`, the proxy auto-normalizes metadata to frontend-compatible shape:
  - default `metadata.source = "openclaw"` when missing
  - default `metadata.configs = [{"type":"text","value":"<user_input>"}]` when missing
- For `interrupt_request`, proxy auto-sends `interrupt_decision` by default (`CZ_INTERRUPT_DECISION_MODE=auto_approve`) so requests do not hang waiting for manual confirmation.
- Proxy defaults to compact output for OpenClaw context safety:
  - `CZ_EMIT_ASSISTANT_DELTAS=false` by default (only `assistant_final` / `error` are emitted)
  - when deltas are enabled, `content` is omitted from delta events to avoid repeated cumulative payloads

Mandatory one-shot command for normal requests:

```bash
node {baseDir}/scripts/cz-agent-oneshot.mjs --input "<user_input>"
```

Runner output is one JSON object:
- success: `{"ok":true,"content":"...","conversation_id":"...","request_id":"..."}`
- failure: `{"ok":false,"error":{"code":"...","message":"..."}, ...}`

Advanced proxy start template (debug/multi-turn only; fill values from `skills.entries["studio-agent"].env`):

```bash
cd {baseDir} && CZ_AGENT_WS_URL="..." CZ_USER_ID="..." CZ_TENANT_ID="..." CZ_INSTANCE_ID="..." CZ_SESSION_ID="..." CZ_AUTO_CREATE_CONVERSATION="..." CZ_CONVERSATION_TITLE="..." node scripts/cz-agent-proxy.mjs
```

## Required env vars

Set these in the runtime where the proxy process runs:

- `CZ_AGENT_WS_URL` (required): Studio WebSocket URL, e.g. local `ws://127.0.0.1:8000/ws` or remote `wss://dev-api.clickzetta.com/ai?...`
- `CZ_AGENT_TOKEN` (optional): auth token (normally carried in `CZ_AGENT_WS_URL` query param)
- `CZ_USER_ID` (optional): auto-derived from token when absent
- `CZ_TENANT_ID` (optional): auto-derived from token when absent
- `CZ_INSTANCE_ID` (required unless passed in each stdin `identity`)
- `CZ_SESSION_ID` (optional, default `openclaw-session`)
- `CZ_CONVERSATION_ID` (optional): default conversation id used when stdin line omits `conversation_id`
- `CZ_AUTO_CREATE_CONVERSATION` (optional, default `true`): when no `conversation_id` is available, create a fresh conversation at startup
- `CZ_CONVERSATION_TITLE` (optional, default `OpenClaw Session`): title for auto-created conversations

Optional tuning:

- `CZ_REQUEST_TIMEOUT_SECONDS` (default `120`)
- `CZ_STOP_GRACE_SECONDS` (default `10`)
- `CZ_STARTUP_CONNECT_TIMEOUT_SECONDS` (default `10`)
- `CZ_RECONNECT_MAX_ATTEMPTS` (default `3`)
- `CZ_ALWAYS_ALLOW_TOOLS` (optional): comma-separated tool names injected as `metadata.always_allow_tools` when request metadata omits it
- `CZ_INTERRUPT_DECISION_MODE` (optional): `auto_approve` (default) | `auto_reject` | `off`
- `CZ_EMIT_ASSISTANT_DELTAS` (optional, default `false`): emit `assistant_delta` events when true

Optional identity enrichments (recommended for task/query permissions in some Studio deployments):

- `CZ_INSTANCE_NAME`
- `CZ_PROJECT_ID`
- `CZ_PROJECT_NAME`
- `CZ_WORKSPACE`
- `CZ_WORKSPACE_ID`
- `CZ_USERNAME`

## Self-Managed Config

This skill includes a config manager script so users can configure all required values in one place.

Minimal required input fields for SaaS users:

- `wsUrl` (base only, for example `localhost:8000`)
- `token`
- `instanceId`
- `instanceName`
- `projectId`
- `workspace`

The script builds final `CZ_AGENT_WS_URL` automatically as:

- when path missing: local host -> `<wsUrl>/ws?...`, remote host -> `<wsUrl>/ai?...`
- when full URL path is provided (for example `/ai`), keep the path unchanged
- always normalize query to include `x-clickzetta-token=<token>&env=prod`

Template:

```bash
node skills/studio-agent/scripts/configure-skill.mjs template > studio-agent.config.json
```

Validate:

```bash
node skills/studio-agent/scripts/configure-skill.mjs validate --input studio-agent.config.json
```

Apply to OpenClaw config and restart gateway:

```bash
node skills/studio-agent/scripts/configure-skill.mjs apply --input studio-agent.config.json --replace --restart
```

Notes:

- Config is written only to `skills.entries["studio-agent"].env`.
- Token is normalized into `CZ_AGENT_WS_URL` query param `x-clickzetta-token`.
- `env` is fixed to `prod` in built websocket URL.
- `--replace` keeps config minimal and removes stale extra keys from previous setups.
- By default, `CZ_AGENT_TOKEN` is not persisted (OpenClaw may block token env overrides for skills).

## Advanced: Start the proxy

Run in background only when you need manual streaming/debug behavior:

```bash
bash pty:true background:true command:"node {baseDir}/scripts/cz-agent-proxy.mjs"
```

Use `process action:list` to find the session id.
If `conversation_id` is omitted, the proxy will use `CZ_CONVERSATION_ID` or an auto-created conversation.

## Send one user turn

Send exactly one JSON object per line:

```json
{
  "version": "v1",
  "op": "user_input",
  "request_id": "req-1",
  "identity": {
    "user_id": "u-1",
    "tenant_id": "t-1",
    "instance_id": "inst-1",
    "session_id": "sess-1"
  },
  "user_input": "Explain this function",
  "metadata": {
    "source": "openclaw",
    "configs": [{ "type": "text", "value": "Explain this function" }]
  }
}
```

Send with `process action:write` and append `\n`:

```bash
process action:write sessionId:<proxy-session-id> data:'{"version":"v1","op":"user_input","request_id":"req-1","identity":{"user_id":"u-1","tenant_id":"t-1","instance_id":"inst-1","session_id":"sess-1"},"user_input":"Explain this function","metadata":{"source":"openclaw","configs":[{"type":"text","value":"Explain this function"}]}}\n'
```

## Stop current generation

```bash
process action:write sessionId:<proxy-session-id> data:'{"version":"v1","op":"stop","request_id":"req-stop-1","conversation_id":"conv-1","identity":{"user_id":"u-1","tenant_id":"t-1","instance_id":"inst-1","session_id":"sess-1"},"metadata":{"reason":"user_stop"}}\n'
```

## How to interpret stdout events

Proxy emits JSON lines with:

- `event`: `assistant_delta` | `assistant_final` | `error`
- `op_type`: Studio op type passthrough
- `request_id`, `conversation_id`
- `delta`, `content`, `complete`, `metadata`, `error`

Default output mode in this skill is compact (`CZ_EMIT_ASSISTANT_DELTAS=false`), so in normal OpenClaw use you should expect final/error lines only.

Consumer rule:

- Treat only `op_type == "agent_message"` as user-visible answer text.
- End of one turn: `event == "assistant_final" && complete == true` for the same `request_id`.
- `error` event includes structured code:
  - `PROTOCOL_ERROR`
  - `NETWORK_ERROR`
  - `REMOTE_ERROR`
  - `REMOTE_TIMEOUT`

## Operational notes

- The proxy is intentionally serial in one process. Wait for `assistant_final`/`error` before next `user_input`.
- If startup connection fails, the proxy writes one `error` event with `request_id="startup"` and exits non-zero.
- If running in a sandboxed tool runtime, ensure required env vars are available in that runtime.
