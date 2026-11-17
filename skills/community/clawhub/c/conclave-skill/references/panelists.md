# Panelist Roster

Six AI panelists + one external advisor. All CLI calls require `no_proxy='*'` prepended.

## 1. Hermes (Chair & Panelist)

- This agent itself. Positioning and rebuttals are drafted in-session by the chair, written to disk in the same format as the other four.
- Red line: must not favor itself; views struck down are still recorded under "rejected positions".

## 2. Claude Code

- Command: `no_proxy='*' claude -p '<prompt>' --max-turns 1`
- Auth: official OAuth (zhang@testsprite.com), credentials stored in macOS login keychain.
  Background sessions may fail to read the keychain (security exit 36).
  **DO NOT put passwords in prompts or scripts.** The user must manually unlock the keychain in an interactive terminal before starting a background debate session (macOS only; N/A on Linux/Windows where only `~/.claude/.credentials.json` is checked):
  ```
  security unlock-keychain ~/Library/Keychains/login.keychain-db
  ```
  If still 401: check for and move aside old `~/.claude/.credentials.json`, then retry.
- Update: `claude update`
- Install: `npm install -g @anthropic-ai/claude-code` (or run `scripts/install.sh` to install everything at once)
- Ping: `no_proxy='*' claude -p 'reply with one word: pong' --max-turns 1`

## 3. Codex

- Command: `no_proxy='*' codex exec --skip-git-repo-check -c model_reasoning_effort="medium" '<prompt>'`
  For important sessions, replace medium with xhigh.
- Auth: cmdme.cn relay, sk- key in `~/.codex/auth.json`; in config.toml set
  `requires_openai_auth = false`, `wire_api = "responses"`, `base_url = "https://cmdme.cn"`.
- Pitfall: exec defaults to a read-only sandbox; file writes are rejected → prompts must require "full text to stdout",
  and the chair extracts the output via `process(action='log', offset=0, limit=400)` to disk.
- Update: `codex update` (or `npm install -g @openai/codex@latest` when npm-managed)
- Install: `npm install -g @openai/codex`
- Ping: `no_proxy='*' codex exec --skip-git-repo-check 'reply with one word: pong'`

## 4. Gemini CLI

- Command: `no_proxy='*' GEMINI_CLI_TRUST_WORKSPACE=true zsh -i -c 'gemini -p "<prompt>"'`
  (On Linux/Windows without zsh, preflight.sh auto-falls back to `bash -i -c` — both source rc files for env keys.)
- Pitfall: since 0.55.1 a trust-directory check was added; non-interactive calls must carry `GEMINI_CLI_TRUST_WORKSPACE=true`, otherwise the CLI refuses to run.
- Auth / env: `GOOGLE_GEMINI_BASE_URL` + `GEMINI_API_KEY` (persisted in user shell rc).
  Key format determines provider: `AQ.Ab8…` = Google official (base generativelanguage.googleapis.com),
  `sk-…` = cmdme relay. Mixing them causes 401.
  Note: non-interactive shells may not read rc files — call via `zsh -i -c` or explicitly export variables.
- Update: `npm install -g @google/gemini-cli@latest`
- Install: `npm install -g @google/gemini-cli`
- Ping: `no_proxy='*' GEMINI_CLI_TRUST_WORKSPACE=true zsh -i -c 'gemini -p "reply with one word: pong"'`

## 5. Qwen

- Command: `no_proxy='*' qwen -p '<prompt>'`
- Binary lives in ~/.local/lib/qwen-code (official installer layout).
- Update: `npm install -g @qwen-code/qwen-code@latest` when npm-managed; otherwise `qwen update`
- Install: `npm install -g @qwen-code/qwen-code`
- Ping: `no_proxy='*' qwen -p 'reply with one word: pong'`

## 6. DeepSeek (deepcode-panelist)

- **Note**: The `deepcode` CLI itself is TTY-locked (requires an interactive terminal). For non-interactive / background debates, use the `deepcode-panelist` wrapper instead.
- Command: `deepcode-panelist '<prompt>'`
- Wrapper path: `/Users/mac/.local/bin/deepcode-panelist`
- What it does: reads `~/.deepcode/settings.json` (model, API key, base URL, reasoning effort), then calls the Ark Responses API directly — same backend as the TUI, zero ANSI overhead, pure text output.
- Config source (`~/.deepcode/settings.json`):
  ```json
  {
    "env": {
      "MODEL": "deepseek-v4-flash-ga-260731",
      "BASE_URL": "https://ark.cn-beijing.volces.com/api/v3",
      "API_KEY": "ark-..."
    },
    "thinkingEnabled": true,
    "reasoningEffort": "max"
  }
  ```
- Output: model text to stdout; reasoning chain + usage metadata to stderr.
- Install wrapper (one-time):
  ```bash
  # The wrapper is a shell script; copy it to PATH
  cp /path/to/deepcode-panelist /Users/mac/.local/bin/
  chmod +x /Users/mac/.local/bin/deepcode-panelist
  ```
- Install deepcode (for config generation + interactive use):
  ```bash
  npm i -g deepcode
  deepcode --version   # v0.1.34
  # Then run interactively once to create ~/.deepcode/settings.json
  ```
- Ping: `deepcode-panelist 'reply with one word: pong'`
- Pitfall: `deepcode -p` without the wrapper fails with "requires an interactive terminal (TTY)" — this is by design in the upstream CLI. The wrapper is the canonical non-interactive path.

## 7. Manus (External Advisor, async)

- **Privacy warning**: Sending the final draft and round summaries to Manus transmits user problem statements and internal debate content to a third-party service. Do not use Manus for debates containing proprietary, personal, or regulated data unless you have reviewed Manus's data-handling policy and obtained appropriate consent.
- Channel: Hermes Manus MCP — `mcp__manus_mcp__create_task` (deferred tool; call tool_describe first, then tool_call).
- Usage: package the final draft + round-summary synthesis into a prompt and create a task; wait for the result (async, may take minutes to tens of minutes).
- Timeout 30 min with no response → skip the advisor step; final report notes "external advisor not reviewed".
- Ping: send a minimal task "reply with one word: pong" (mode="speed"); receiving a task_id means the channel is open.
- 2026-08-12 verified: this MCP only exposes create_task / create_webhook / delete_webhook.
  **There is no MCP tool to query task results. BUT (2026-08-14 verified): the same MANUS_MCP_API_KEY works against the REST API directly, making results fully retrievable without webhooks:**
  - Create: `POST https://api.manus.im/v1/tasks` with header `API_KEY: <key>`, body `{"prompt": "...", "taskMode": "chat"}` → returns `task_id`.
  - Poll: `GET https://api.manus.im/v1/tasks/{task_id}` with the same header every 60s until `status == "completed"`; extract text from `output[]` where `role == "assistant"` → `content[].text`.
  - Typical review turnaround: ~3 minutes. This is the preferred path on CLI-only machines; keep the webhook/user-paste routes as fallbacks only.

## General Rules

1. All calls are non-interactive (`-p` / `exec`), no TUI; use `terminal(background=true, notify_on_complete=true)` when parallelizing.
2. Long texts go to disk; prompts only give paths.
3. Any disconnection: immediate identical retry; 2 consecutive failures → mark absent, note in final report.
4. On a new machine or after any CLI failure, run `scripts/install.sh` first — it detects and installs all CLIs/dependencies, then lists exactly which provider keys the user must configure. Pre-flight `scripts/preflight.sh` (update + ignition ping) is mandatory before every debate; do not start until all agents are reachable.
