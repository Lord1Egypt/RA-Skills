---
name: ai-config-admin
description: >-
  Manage AI configuration for OpenClaw, OpenCode, Codex CLI, and Claude Code.
  Use when the user wants to add/remove models or providers, switch default or
  agent models, replace or update OpenClaw/OpenCode/Codex/Claude config files,
  or convert natural-language / irregular JSON / TOML input into the exact
  config changes supported by the bundled scripts. Triggers include:
  openclaw.json, opencode.json, config.toml, auth.json, settings.json, Claude
  Code, Codex CLI, provider, model, default model, agent model,
  OPENAI_API_KEY, ANTHROPIC_AUTH_TOKEN, ANTHROPIC_BASE_URL.
---
# AI Config Admin

Identify which target the user wants to modify first: OpenClaw, OpenCode, Codex CLI, or Claude Code. Then use the bundled script for that target.

## Required rules

- Follow this skill and the existing script capabilities exactly.
- Do not manually edit config files to bypass script limitations.
- If the request is outside current script support, say so clearly and explain what is missing.
- Before every write, create a backup in the same directory as the original file.
- Perform backup and write through the bundled script, not manual editing.
- Do not echo secrets such as `apiKey`, `OPENAI_API_KEY`, `ANTHROPIC_AUTH_TOKEN`, tokens, or refresh tokens in replies.

## Target files

- OpenClaw: `~/.openclaw/openclaw.json`
- OpenCode: `~/.config/opencode/opencode.json`
- Codex CLI: `~/.codex/config.toml`, `~/.codex/auth.json`
- Claude Code: `~/.claude/settings.json`

## Routing

- OpenClaw requests: `openclaw.json`, default model, agent model, add/remove provider, add/remove model, memory search.
- OpenCode requests: `opencode.json`, OpenCode config, replace full JSON.
- Codex CLI requests: `config.toml`, `auth.json`, Codex CLI, `model_provider`, `review_model`, `wire_api`, `requires_openai_auth`.
- Claude Code requests: `settings.json`, Claude Code, `ANTHROPIC_AUTH_TOKEN`, `ANTHROPIC_BASE_URL`, `ANTHROPIC_MODEL`, `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC`, `CLAUDE_CODE_ATTRIBUTION_HEADER`.

## Input handling

- Accept natural language, semi-structured JSON, or mixed descriptions.
- Convert user intent into explicit script parameters or complete JSON/TOML text before invoking scripts.
- Ask follow-up questions only when critical parameters cannot be inferred.

### OpenClaw

- Infer supported arguments from user intent.
- When fields are missing, prefer filling from the current config when safe.
- Use `add-model` to add a model to an existing provider, or to create/update a provider when the user also supplies the required provider fields.
- For a brand-new provider, `add-model` needs enough provider config to make it valid: at minimum `--base-url` and `--api`; use `--api-key` and `--auth-header` when appropriate.
- Use `add-openai-model` only for OpenAI-compatible provider setup flows that require explicit `apiKey` and `api` handling in one step.

### OpenCode

- If the user provides complete JSON, replace the file directly.
- Do not merge partial JSON.

### Codex CLI

- `config.toml`: infer structured parameters and call the script.
- `auth.json`: write only when the user provides a complete JSON payload; default to full replacement.
- Do not delete unknown TOML sections such as `projects`, `notice`, or `tui`.
- If existing `auth.json` contains login-state fields, replace it only when the user explicitly asks for full replacement.

### Claude Code

- Full `settings.json` input may be replaced directly.
- If the user provides only an `{"env": {...}}` fragment:
  - If `ANTHROPIC_BASE_URL` is present, replace the Claude-related env key set.
  - Otherwise, update only the explicitly provided Claude-related env keys.
- Do not invent missing model fields.
- Do not modify non-Claude env keys.

## Commands

Use `{baseDir}` as the skill root.

### OpenClaw

```bash
python3 {baseDir}/scripts/openclaw_config.py --help
python3 {baseDir}/scripts/openclaw_config.py --file ~/.openclaw/openclaw.json summary
python3 {baseDir}/scripts/openclaw_config.py --file ~/.openclaw/openclaw.json add-model \
  --provider-id minimax-cn \
  --model-id MiniMax-M2.7 \
  --name 'MiniMax M2.7' \
  --context-window 200000 \
  --max-tokens 8192 \
  --set-default
```

Supported operations:

- `summary`
- `add-model [--provider-id ...] [--model-id ...] [--name ...] [--context-window ...] [--max-tokens ...] [--reasoning true|false] [--allowlist] [--set-default] [--input text|image ...] [--base-url ...] [--api-key ...] [--api ...] [--auth-header true|false]`
- `add-openai-model ...`
- `set-openai-provider [--base-url ...] [--api-key ...]`
- `remove-model <provider/model>`
- `set-memory-search on|off`
- `set-default-model <modelId>`
- `set-agent-model <agentId> <modelId>`
- `remove-provider <providerId>`

### OpenCode

```bash
python3 {baseDir}/scripts/opencode_config.py --file ~/.config/opencode/opencode.json summary
python3 {baseDir}/scripts/opencode_config.py --file ~/.config/opencode/opencode.json replace-from-stdin <<'EOF'
{...full JSON...}
EOF
```

Supported operations:

- `summary`
- `replace-from-stdin`

### Codex CLI

```bash
python3 {baseDir}/scripts/codex_config.py --help
python3 {baseDir}/scripts/codex_config.py --config-file ~/.codex/config.toml --auth-file ~/.codex/auth.json summary
python3 {baseDir}/scripts/codex_config.py --config-file ~/.codex/config.toml replace-config-from-stdin <<'EOF'
model_provider = "OpenAI"
model = "gpt-5.4"
EOF
python3 {baseDir}/scripts/codex_config.py --auth-file ~/.codex/auth.json replace-auth-from-stdin <<'EOF'
{"OPENAI_API_KEY":"sk-..."}
EOF
```

Supported operations:

- `summary`
- `replace-config-from-stdin`
- `replace-auth-from-stdin`
- `set-openai-provider [--model-provider ...] [--model ...] [--review-model ...] [--reasoning-effort ...] [--disable-response-storage true|false] [--network-access ...] [--windows-wsl-setup-acknowledged true|false] [--model-context-window ...] [--model-auto-compact-token-limit ...] [--provider-name ...] [--base-url ...] [--wire-api ...] [--requires-openai-auth true|false]`

### Claude Code

```bash
python3 {baseDir}/scripts/claude_config.py --help
python3 {baseDir}/scripts/claude_config.py --file ~/.claude/settings.json summary
python3 {baseDir}/scripts/claude_config.py --file ~/.claude/settings.json set-env \
  --anthropic-auth-token 'sk-...' \
  --attribution-header '0'
python3 {baseDir}/scripts/claude_config.py --file ~/.claude/settings.json replace-env \
  --anthropic-base-url 'https://example.invalid' \
  --anthropic-auth-token 'sk-...' \
  --attribution-header '0'
python3 {baseDir}/scripts/claude_config.py --file ~/.claude/settings.json replace-from-stdin <<'EOF'
{"env":{"ANTHROPIC_BASE_URL":"https://example.invalid"}}
EOF
```

Supported operations:

- `summary`
- `replace-from-stdin`
- `set-env [--anthropic-auth-token ...] [--anthropic-base-url ...] [--anthropic-default-haiku-model ...] [--anthropic-default-opus-model ...] [--anthropic-default-sonnet-model ...] [--anthropic-model ...] [--api-timeout-ms ...] [--disable-nonessential-traffic ...] [--attribution-header ...]`
- `replace-env [--anthropic-auth-token ...] [--anthropic-base-url ...] [--anthropic-default-haiku-model ...] [--anthropic-default-opus-model ...] [--anthropic-default-sonnet-model ...] [--anthropic-model ...] [--api-timeout-ms ...] [--disable-nonessential-traffic ...] [--attribution-header ...]`

## Defaults and safeguards

- Do not write `headers.User-Agent` unless explicitly needed.
- Do not switch the default model unless the user asks.
- Do not change `memorySearch` unless the user asks.
- Stop if the script reports validation or dependency errors.
- For OpenCode, default to full replacement when complete JSON is provided.
- For Claude Code, if `ANTHROPIC_BASE_URL` is present, rebuild the Claude-related env set instead of carrying forward stale provider-specific env/model keys.
