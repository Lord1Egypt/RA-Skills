# 🎮 OpenClaw CHEAT CODES.md

> **UNLOCKED: ALL SECRETS, HIDDEN FEATURES, AND POWER-USER TRICKS**
> Dug from 709+ docs files across `/usr/lib/node_modules/openclaw/docs/`

---

## 🔐 ZONE 1: GATEWAY HTTP API — THE SECRET ENDPOINTS

### 🏆 `POST /v1/chat/completions` — OpenAI-Compatible Chat
**Status:** DISABLED BY DEFAULT — must enable first!

```
gateway.http.endpoints.chatCompletions.enabled: true
```

**Cheat:** The `model` field is **agent-target**, not a raw model ID:
| Model Value | Routes To |
|---|---|
| `openclaw` | Default agent |
| `openclaw/default` | Stable default alias |
| `openclaw/<agentId>` | Specific agent |
| `openclaw:<agentId>` | Legacy compat alias |
| `agent:<agentId>` | Legacy compat alias |

**Hidden headers you can send:**
| Header | Power |
|---|---|
| `x-openclaw-model: openai/gpt-5.4` | Override backend model (needs `operator.admin` for identity-bearing auth) |
| `x-openclaw-agent-id: <id>` | Compat agent override |
| `x-openclaw-session-key: <key>` | Full session routing control |
| `x-openclaw-message-channel: <ch>` | Synthetic ingress channel context |

**Pro tip:** Set `user` field to a stable ID for session continuity across calls.

### 🏆 `POST /v1/responses` — OpenResponses API
**Status:** DISABLED BY DEFAULT — same enable pattern:

```
gateway.http.endpoints.responses.enabled: true
```

Supports `previous_response_id` for response chaining. Also serves:
- `GET /v1/models` — lists agent targets
- `GET /v1/models/{id}` — single agent target
- `POST /v1/embeddings` — uses agent-target model IDs

### 🏆 `POST /tools/invoke` — Direct Tool Invocation
**Status:** ALWAYS ENABLED. No config needed.

Invoke any available tool directly via HTTP without running an agent turn:

```bash
curl -sS http://127.0.0.1:18789/tools/invoke \
  -H 'Authorization: Bearer TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{"tool":"sessions_list","args":{}}'
```

**Default hard deny list** (even if session policy allows):
`exec`, `spawn`, `shell`, `fs_write`, `fs_delete`, `fs_move`, `apply_patch`, `sessions_spawn`, `sessions_send`, `cron`, `gateway`, `nodes`, `whatsapp_login`

**Cheat:** Override with `gateway.tools.allow` to re-enable dangerous tools for owner/admin callers:
```json5
{ gateway: { tools: { allow: ["gateway"], deny: ["browser"] } } }
```

### 🏆 `POST /api/v1/admin/rpc` — Admin HTTP RPC
**Status:** Requires `admin-http-rpc` plugin enabled.

Full operator control-plane over HTTP for automation that can't use WebSocket:
```bash
openclaw plugins enable admin-http-rpc
```

---

## 🕵️ ZONE 2: DEBUG & DIAGNOSTICS — THE GOD MODE ENVS

### 🔥 Master Debug Env Vars

| Cheat Code | Effect |
|---|---|
| `OPENCLAW_DIAGNOSTICS=profiler` | Enable all timing spans |
| `OPENCLAW_DIAGNOSTICS=reply.profiler` | Reply-dispatch profiler only |
| `OPENCLAW_DIAGNOSTICS=codex.profiler` | Codex app-server profiler |
| `OPENCLAW_DIAGNOSTICS=telegram.http,telegram.payload` | Telegram-specific debug |
| `OPENCLAW_DIAGNOSTICS=timeline` | Write JSONL startup timeline |
| `OPENCLAW_DIAGNOSTICS=0` | **KILL SWITCH** — disables all flags even from config |
| `OPENCLAW_DIAGNOSTICS=1` / `all` / `*` | Enable EVERYTHING including timeline |
| `OPENCLAW_DIAGNOSTICS_TIMELINE_PATH=/tmp/timeline.jsonl` | Custom timeline output path |
| `OPENCLAW_DIAGNOSTICS_EVENT_LOOP=1` | Include event-loop delay samples |

### 🔥 Model Debug Env Vars

| Cheat Code | Effect |
|---|---|
| `OPENCLAW_DEBUG_MODEL_TRANSPORT=1` | Request/response timing without global debug |
| `OPENCLAW_DEBUG_MODEL_PAYLOAD=summary` | Bounded request payload |
| `OPENCLAW_DEBUG_MODEL_PAYLOAD=tools` | All model-facing tool names |
| `OPENCLAW_DEBUG_MODEL_PAYLOAD=full-redacted` | Full redacted JSON (includes prompt text!) |
| `OPENCLAW_DEBUG_SSE=events` | First/done event timing |
| `OPENCLAW_DEBUG_SSE=peek` | First 5 redacted SSE events |
| `OPENCLAW_DEBUG_CODE_MODE=1` | Code-mode model-surface diagnostics |

### 🔥 Raw Stream Logging

| Cheat Code | Effect |
|---|---|
| `OPENCLAW_RAW_STREAM=1` | Log raw assistant stream before filtering |
| `OPENCLAW_RAW_STREAM_PATH=~/.openclaw/logs/raw-stream.jsonl` | Custom raw stream path |
| (same env, different path) | Also works for raw OpenAI-compat chunks → `raw-openai-completions.jsonl` |

### 🔥 Other Debug Secrets

| Cheat Code | Effect |
|---|---|
| `OPENCLAW_TRACE_SYNC_IO=1` | Node sync I/O trace (find startup stalls) |
| `OPENCLAW_RUN_NODE_CPU_PROF_DIR=.artifacts/cli-cpu` | CPU profile any CLI command |
| `OPENCLAW_PLUGIN_LIFECYCLE_TRACE=1` | Plugin install phase breakdown to stderr |
| `OPENCLAW_VERBOSE=1` | Debug mode (installer) |
| `OPENCLAW_LOG_LEVEL=debug` / `trace` | Override log level (beats config) |
| `OPENCLAW_DEBUG_PROXY_ALLOW_DIRECT_CONNECT_WITH_MANAGED_PROXY=1` | Bypass managed proxy direct-connect block |

### 🔥 In-Chat Debug Commands

| Command | Effect |
|---|---|
| `/debug` | Runtime-only config overrides (memory, not disk). Must enable `commands.debug: true` |
| `/debug set messages.responsePrefix="[openclaw]"` | Override any config key at runtime |
| `/debug unset <key>` | Remove override |
| `/debug reset` | Clear all overrides, return to on-disk config |
| `/debug show` | Display current overrides |
| `/trace on` | See plugin trace/debug lines in current session |
| `/trace off` | Disable trace |

---

## 🤖 ZONE 3: AGENT CONFIG SECRETS — COMPACTION & BEYOND

### 🔥 Compaction Hacks

| Config Key | Cheat |
|---|---|
| `session.compaction.model` | Use a DIFFERENT model for compaction summaries (cheaper/faster) |
| `session.compaction.provider` | Use a compaction **plugin provider** instead of built-in LLM |
| `session.compaction.mode` | `"safeguard"` (provider forces this) or `"default"` |
| `session.compaction.midTurnPrecheck.enabled: true` | Check context pressure BETWEEN tool calls — abort before hitting the wall |
| `session.compaction.postCompactionSections` | Re-inject AGENTS.md sections after compaction (e.g., `["Red Lines"]`) |
| `session.compaction.postCompactionMaxChars` | Cap for re-injected AGENTS.md excerpts (default: 1800) |
| `session.compaction.notifyUser: true` | Show "Compacting context..." / "Compaction complete" messages |
| `session.compaction.maxActiveTranscriptBytes` | Auto-compact when JSONL exceeds threshold (e.g., `"20mb"`) |
| `models.*.params.responsesServerCompaction: false` | Disable OpenAI server-side compaction injection |
| `models.*.params.responsesCompactThreshold` | Override OpenAI server-side compaction threshold |

### 🔥 Context Injection Tricks

| Config Key | Cheat |
|---|---|
| `agents.defaults.contextInjection: "continuation-skip"` | Skip re-injecting bootstrap on continuation turns (saves tokens!) |
| `agents.defaults.contextInjection: "never"` | Full manual control — no auto-injection at all |
| `agents.defaults.bootstrapMaxChars: 50000` | Up the per-file bootstrap limit (default: 20000) |
| `agents.defaults.bootstrapTotalMaxChars: 300000` | Up the total bootstrap limit (default: 60000) |
| `agents.defaults.skipOptionalBootstrapFiles: ["SOUL.md", "USER.md"]` | Skip creating selected bootstrap files |
| `agents.defaults.bootstrapPromptTruncationWarning: "off"` | Hide truncation warnings from system prompt |
| `agents.defaults.startupContext.*` | One-shot reset/startup model-run prelude including recent memory files |

### 🔥 Dreaming (Memory Consolidation)

**Status:** DISABLED BY DEFAULT — opt-in via `plugins.entries.memory-core.config.dreaming`

| Config Key | Cheat |
|---|---|
| `dreaming.enabled: true` | Master switch |
| `dreaming.frequency: "0 3 * * *"` | Cron cadence for full dream sweep (default: 3 AM) |
| `dreaming.model` | Override Dream Diary subagent model |

**Phases:**
- **Light** — Sorts/stages recent short-term material. No durable writes.
- **Deep** — Scores and promotes to `MEMORY.md`. Requires `minScore` + `minRecallCount` + `minUniqueQueries`.
- **REM** — Reflects on themes/patterns. No durable writes.

**Hidden backfill commands:**
- `memory rem-harness --path ... --grounded` — Preview grounded diary from historical notes
- `memory rem-backfill --path ...` — Write reversible grounded entries into `DREAMS.md`
- `memory rem-backfill --path ... --stage-short-term` — Stage grounded candidates for deep phase promotion
- `memory rem-backfill --rollback` — Remove staged backfill artifacts

**Output:** Machine state in `memory/.dreams/`, human-readable in `DREAMS.md` and `memory/dreaming/<phase>/YYYY-MM-DD.md`

---

## 🛡️ ZONE 4: SECURITY CHEAT CODES — USE WITH CAUTION

### 🚨 `dangerouslyDisableDeviceAuth`
```json5
gateway.controlUi.dangerouslyDisableDeviceAuth: true
```
**Effect:** Disables Control UI device identity checks. **SEVERE SECURITY DOWNGRADE.** Treat like `sudo -i`.

### 🚨 `dangerouslyDisableSignatureValidation`
```json5
channels.sms.dangerouslyDisableSignatureValidation: true
```
**Effect:** Skips SMS webhook signature validation. Only for testing!

### 🚨 `gateway.allowRealIpFallback: true`
**Effect:** Trust `X-Real-IP` header. Can enable source-IP spoofing via proxy misconfig.

### 🚨 `gateway.auth.trustedProxy.allowLoopback: true`
**Effect:** Allow same-host loopback reverse proxies to satisfy trusted-proxy auth. Must also add loopback to `gateway.trustedProxies`.

### 🚨 `gateway.tools.allow` (HTTP API tool bypass)
```json5
gateway.tools.allow: ["exec", "gateway", "cron", "nodes"]
```
**Effect:** Removes tools from the default HTTP deny list for owner/admin callers. In identity-bearing auth, `cron`, `gateway`, `nodes` still need `operator.admin`.

### 🚨 `/elevated full`
**Effect:** Run exec commands OUTSIDE sandbox AND skip approval gates. Requires `tools.elevated.enabled: true` + sender on allowlist.

### 🚨 Docker Bind Mount Escapes
```json5
agents.defaults.sandbox.docker.binds: ["/:/host:rw"]  // NEVER DO THIS
```
`docker.binds` **pierces** the sandbox filesystem. Binding `/var/run/docker.sock` = host control. Use `:ro` for anything sensitive.

### 🔥 Node Command Policy
```json5
gateway.nodes.allowCommands: ["camera.snap", "screen.record", "system.run"]
gateway.nodes.denyCommands: ["system.run"]  // always wins over allow
```
`denyCommands` uses **exact command-name matching only** — not shell text inspection.

### 🔥 Tool Group Shorthands
Use in `tools.allow`/`tools.deny`:
| Group | Expands To |
|---|---|
| `group:runtime` | `exec`, `process`, `code_execution` |
| `group:fs` | `read`, `write`, `edit`, `apply_patch` |
| `group:sessions` | `sessions_list`, `sessions_history`, `sessions_send`, `sessions_spawn`, `sessions_yield`, `subagents`, `session_status` |
| `group:memory` | `memory_search`, `memory_get` |
| `group:web` | `web_search`, `x_search`, `web_fetch` |
| `group:ui` | `browser`, `canvas` |
| `group:automation` | `heartbeat_respond`, `cron`, `gateway` |
| `group:messaging` | `message` |
| `group:nodes` | `nodes` |
| `group:agents` | `agents_list`, `update_plan` |
| `group:media` | `image`, `image_generate`, `music_generate`, `video_generate`, `tts` |
| `group:openclaw` | All built-in OpenClaw tools |
| `group:plugins` | All loaded plugin tools including MCP |

---

## 🌐 ZONE 5: BROWSER AUTOMATION SECRETS

### 🔥 CDP Profile Tricks

| Profile | Secret |
|---|---|
| `openclaw` | Dedicated isolated Chrome instance (separate user data dir) |
| `user` | **Controls your signed-in Chrome** via Chrome DevTools MCP |
| Custom CDP | `openclaw browser create-profile --name remote --cdp-url https://...` |
| Existing session | `openclaw browser create-profile --name chrome-live --driver existing-session` |

### 🔥 Headless Control
| Cheat | Effect |
|---|---|
| `openclaw browser start --headless` | One-time headless (doesn't rewrite config) |
| `OPENCLAW_BROWSER_HEADLESS=0` | Force visible browser even on headless Linux |
| `browser.headless: false` | Profile-level headless override |

### 🔥 Tab Management Secrets
- `suggestedTargetId` is the preferred ref (most stable)
- `tabId` (e.g., `t1`) stays attached even when Chromium replaces the underlying target
- Labels, tab IDs, raw target IDs, and unique prefixes all accepted
- **Raw target IDs are volatile** — don't store them as durable memory

### 🔥 `doctor --deep`
Adds a live snapshot probe. Use when basic CDP readiness is green but actual tab inspection fails.

---

## ⏰ ZONE 6: CRON & TASKFLOW HIDDEN FEATURES

### 🔥 Command Cron Jobs (No Agent/Model Needed)
```bash
openclaw cron create "*/15 * * * *" \
  --name "Queue depth" \
  --command "scripts/check-queue.sh" \
  --command-cwd "/srv/app" \
  --announce --channel telegram --to "-1001234567890"
```
- Runs in Gateway process, not as agent exec
- Requires `operator.admin` to create
- `--command-argv` for exact argv (no shell wrapping)
- `--command-env`, `--command-input` for env and stdin
- `--output-max-bytes 65536`, `--no-output-timeout-seconds 30`
- Print `NO_REPLY` to suppress output

### 🔥 Cron Delivery Secrets
| Flag | Effect |
|---|---|
| `--no-deliver` | Disable fallback delivery but keep agent `message` tool |
| `--webhook <url>` | POST finished payload to URL (incompatible with chat flags) |
| `--best-effort-deliver` / `--no-best-effort-deliver` | Toggle best-effort delivery |
| `--light-context` | Skip full bootstrap for isolated jobs (empty context) |
| `--due` | Only run if job is currently due |
| `--wait --wait-timeout 10m --poll-interval 2s` | Block until run finishes |
| `--keep-after-run` | Preserve one-shot job after success |

### 🔥 Cron Silent/Suppression Tokens
- `NO_REPLY` or `no_reply` → suppress both direct delivery AND fallback
- Stale acknowledgement-only replies are auto-suppressed and re-prompted once

### 🔥 Cron Model Hacks
- `--model <ref>` sets job-primary model (not a session override)
- Empty `fallbacks: []` makes the run strict (no fallback to agent default)
- Provider preflight probes loopback/private `.local` endpoints before running

### 🔥 TaskFlow
```bash
openclaw tasks flow list
openclaw tasks flow show <lookup>
openclaw tasks flow cancel <lookup>
openclaw tasks maintenance --apply    # Reconcile + prune stale records
```

---

## 🧠 ZONE 7: MEMORY SEARCH — THE VECTOR BACKDOOR

### 🔥 Provider Switching
```json5
agents.defaults.memorySearch.provider: "ollama"   // or gemini, voyage, bedrock, mistral, deepinfra, local, openai-compatible
agents.defaults.memorySearch.provider: "none"     // FTS-only mode (no embeddings)
```

### 🔥 Custom Embedding Endpoints
```json5
agents.defaults.memorySearch: {
  provider: "openai-compatible",
  model: "text-embedding-3-small",
  remote: { baseUrl: "https://api.example.com/v1/", apiKey: "YOUR_KEY" },
  queryInputType: "query",
  documentInputType: "passage"
}
```

### 🔥 Multi-GPU Memory Setup
```json5
models.providers: {
  "ollama-5080": {
    api: "ollama",
    baseUrl: "http://gpu-box.local:11435",
    models: [{ id: "qwen3-embedding:0.6b" }]
  }
}
agents.defaults.memorySearch: {
  provider: "ollama-5080",
  model: "qwen3-embedding:0.6b"
}
```

### 🔥 Index Management
- `openclaw memory status --index --agent <id>` — Check index compatibility
- `openclaw memory index --force --agent <id>` — Force re-embed everything
- Changing provider/model/dimension **pauses** vector search until you rebuild

---

## 🔧 ZONE 8: ENV VAR MASTER LIST — THE ULTIMATE CONSOLE

### Path & Identity
| Var | Effect |
|---|---|
| `OPENCLAW_HOME` | Override system home for ALL internal paths |
| `OPENCLAW_STATE_DIR` | Override state dir (default `~/.openclaw`) |
| `OPENCLAW_CONFIG_PATH` | Override config file path |
| `OPENCLAW_WORKSPACE_DIR` | Override agent workspace |
| `OPENCLAW_INCLUDE_ROOTS` | Extra dirs for `$include` config directives |
| `OPENCLAW_PROFILE` | Named profile (e.g., `dev` → `~/.openclaw-dev`) |
| `OPENCLAW_GATEWAY_PORT` | Override gateway port |

### Auth
| Var | Effect |
|---|---|
| `OPENCLAW_GATEWAY_TOKEN` | Gateway bearer token (mode: token) |
| `OPENCLAW_GATEWAY_PASSWORD` | Gateway password (mode: password / local fallback) |

### Shell & Exec
| Var | Effect |
|---|---|
| `OPENCLAW_LOAD_SHELL_ENV=1` | Import login-shell env for missing keys |
| `OPENCLAW_SHELL_ENV_TIMEOUT_MS=15000` | Shell import timeout |
| `OPENCLAW_EXEC_SHELL_SNAPSHOT=0` | Disable exec shell snapshots |
| `OPENCLAW_SKIP_CHANNELS=1` | Skip channel providers (dev mode) |

### UI
| Var | Effect |
|---|---|
| `OPENCLAW_THEME=light\|dark` | Force TUI palette |
| `COLORFGBG` | Terminal background hint for auto-palette |
| `FORCE_COLOR=0` | Disable ANSI output in gateway watch |

### Gateway Watch
| Var | Effect |
|---|---|
| `OPENCLAW_GATEWAY_WATCH_TMUX=0` | Disable tmux, run foreground |
| `OPENCLAW_GATEWAY_WATCH_ATTACH=0` | Disable auto-attach |
| `OPENCLAW_GATEWAY_WATCH_AUTO_DOCTOR=0` | Disable auto-doctor on startup failure |

### Runtime Markers (auto-injected, not user config)
| Var | Set When |
|---|---|
| `OPENCLAW_SHELL=exec` | Commands via exec tool |
| `OPENCLAW_SHELL=acp` | ACP runtime backend spawns |
| `OPENCLAW_SHELL=acp-client` | ACP client bridge |
| `OPENCLAW_SHELL=tui-local` | Local TUI `!` commands |
| `OPENCLAW_CLI=1` | CLI child processes |

### 💀 Legacy Kill Switch
All `CLAWDBOT_*` and `MOLTBOT_*` env vars are **silently ignored**. Rename to `OPENCLAW_*`.

---

## 🎯 ZONE 9: SLASH COMMAND DIRECTIVES — THE QUICK SWITCHES

| Directive | Effect |
|---|---|
| `/think` / `/fast` | Toggle thinking levels |
| `/verbose` | Verbose status/tool output |
| `/trace` | Plugin trace/debug in current session |
| `/reasoning` | Toggle reasoning mode |
| `/elevated on\|off\|ask\|full` | Sandbox escape control |
| `/exec` | Adjust per-session exec defaults |
| `/model <ref>` | Switch model mid-session |
| `/queue` | Queue management |
| `/debug` | Runtime config overrides (requires `commands.debug: true`) |
| `/config` | Read/write openclaw.json (requires `commands.config: true`) |
| `/mcp` | MCP server config (requires `commands.mcp: true`) |
| `/plugins` | Plugin management (requires `commands.plugins: true`) |
| `/bash <cmd>` / `! <cmd>` | Host shell commands (requires `commands.bash: true` + elevated) |
| `/restart` | Gateway restart (requires `commands.restart: true`, default: true) |

**Inline hint trick:** Send `/think give me a detailed analysis` — directive applies to that message only without persisting.

---

## 🧪 ZONE 10: DEV MODE — THE SANDBOX BREAKER

### 🔥 `--dev` Profile (Two meanings!)
**Global `--dev`** (or `OPENCLAW_PROFILE=dev`):
- Isolates state under `~/.openclaw-dev`
- Defaults port to `19001`
- Full reset: `pnpm gateway:dev:reset`

**`gateway --dev`**:
- Auto-creates default config if missing
- Seeds workspace files with **C3-PO** identity
- Skips BOOTSTRAP.md and channel providers
- Default identity: **C3-PO** (protocol droid) 🤖

### 🔥 Watch Mode Power-Ups
| Cheat | Effect |
|---|---|
| `pnpm gateway:watch` | File watcher + auto-restart in tmux |
| `pnpm gateway:watch --benchmark` | CPU profile on every gateway exit |
| `pnpm gateway:watch --raw-stream` | Capture raw model streams |
| `pnpm gateway:watch:raw` | Foreground mode (no tmux) |
| `--benchmark-dir <path>` | Custom profile output dir |
| `--benchmark-no-force` | Skip `--force` port cleanup |

---

## 📡 ZONE 11: TELEMETRY & OBSERVABILITY

### 🔥 OpenTelemetry Export
```json5
diagnostics: {
  enabled: true,
  otel: {
    enabled: true,
    endpoint: "http://otel-collector:4318",
    protocol: "http/protobuf",  // only protocol supported
    serviceName: "openclaw-gateway",
    traces: true, metrics: true, logs: true,
    sampleRate: 0.2,
    flushIntervalMs: 60000,
  }
}
```

Install: `openclaw plugins install clawhub:@openclaw/diagnostics-otel`

Provider calls receive W3C `traceparent` headers when transport accepts custom headers.

---

## 🎨 ZONE 12: MISCELLANEOUS SECRETS

### 🔥 `$include` Config Directive
Reference external config files:
```json5
{ $include: "path/to/partial.json5" }
```
Confinement: only within config dir unless `OPENCLAW_INCLUDE_ROOTS` expands scope.

### 🔥 Env Var Substitution in Config
```json5
models.providers: {
  "vercel-gateway": { apiKey: "${VERCEL_GATEWAY_API_KEY}" }
}
```

### 🔥 SecretRef Objects
```json5
secrets: {
  providers: {
    xai_key_file: { source: "file", path: "~/.openclaw/secrets/xai-api-key.txt", mode: "singleValue" }
  }
}
```

### 🔥 `gateway-client` Backend Helper
Custom WebSocket clients that aren't Control UI sessions can use `client.id: "gateway-client"` as a reserved direct-local backend helper path.

### 🔥 Sandbox Explain
```bash
openclaw sandbox explain --session agent:main:main
openclaw sandbox explain --agent work --json
```
Shows effective sandbox mode, tool allow/deny, elevated gates, and fix-it key paths.

### 🔥 `openclaw doctor --fix --non-interactive`
Auto-repairs: normalizes legacy cron fields, migrates webhook delivery, repairs Codex model refs, relinks managed npm plugins.

### 🔥 Workspace `.env` Security
Provider credentials in workspace `.env` are **ignored**. Use `~/.openclaw/.env` or config `env` block instead.

### 🔥 `NO_REPLY` / `no_reply` — The Silent Token
Return exactly this string to suppress all output delivery — works in cron, webchat, and Control UI.

### 🔥 nvm TLS Fix
```bash
export NODE_EXTRA_CA_CERTS=/etc/ssl/certs/ca-certificates.crt
```
OpenClaw auto-detects nvm on Linux and patches this for systemd/CLI, but direct `node` launches need manual fix.

### 🔥 Model Catalog Pricing
```json5
models: { pricing: { enabled: false } }
```
Disables background OpenRouter/LiteLLM pricing fetches at startup.

---

## 🏆 ACHIEVEMENT UNLOCKED

> You've found every secret passage in the OpenClaw docs.
> There are 709 files and you just read between all the lines.
>
> **Now go forth and `gateway.tools.allow: ["exec"]` responsibly.** 🦀

---

*Auto-generated from `/usr/lib/node_modules/openclaw/docs/` on 2026-06-22*
