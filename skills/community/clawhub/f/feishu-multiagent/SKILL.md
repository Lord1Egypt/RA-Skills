---
name: openclaw-feishu-multi-agent-setup
description: Configure OpenClaw multi-agent routing for Feishu multi-account setups. Use when users need two or more Feishu bots (different appId/appSecret) to run on isolated agents/workspaces with distinct system prompts and independent MEMORY bootstrap, or when troubleshooting wrong-agent routing, shared persona, open_id cross-app errors, pairing/account mixups, memory provider failures, contact scope warnings (99991672), or card streaming permission errors.
---

# Openclaw Feishu Multi Agent Setup

## Overview

Set up and verify that each Feishu account is routed to the intended OpenClaw agent with isolated workspace and prompt files.
Apply deterministic checks so routing, persona, and channel health are provable from logs.
Also ensure each new agent has a valid `MEMORY.md` and working memory embeddings.

## Required Inputs

- Target agent ids (example: `main`, `assistant`)
- Target workspace paths (example: `~/.openclaw/workspace`, `~/.openclaw/workspace-assistant`)
- Feishu account ids (example: `default`, `backup`)
- App credentials per account (`appId`, `appSecret`)
- Memory embedding plan per agent (`auto` or explicit provider/endpoint)

## Workflow

### 1. Inspect current state first

Run:

```bash
openclaw agents list --bindings
openclaw agents bindings --json
openclaw config get channels.feishu
```

Detect these issues before changing anything:

- `backup/default` both mapped to same agent
- missing agent in `agents.list`
- missing account in `channels.feishu.accounts`
- duplicated `agentDir` across agents

### 2. Back up config before edits

```bash
cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.bak.$(date +%Y%m%d-%H%M%S)
```

### 3. Ensure agents are isolated

Prefer non-interactive creation when adding a new agent:

```bash
openclaw agents add assistant \
  --non-interactive \
  --workspace ~/.openclaw/workspace-assistant \
  --model minimax-portal/MiniMax-M2.5
```

Ensure `agents.list[]` has unique `workspace` and `agentDir` per agent.

### 4. Bootstrap required workspace files for new agents

For every new non-main agent workspace, verify these files exist and are customized:

- `AGENTS.md`
- `SOUL.md`
- `IDENTITY.md`
- `USER.md`
- `TOOLS.md`
- `MEMORY.md` (or `memory.md`)

Why this is mandatory:

- `MEMORY.md` is injected into system prompt when present.
- Without agent-specific MEMORY bootstrap, global long-term context will be missing from prompt.

Also create daily memory directory (used by memory indexing):

```bash
mkdir -p ~/.openclaw/workspace-assistant/memory
```

### 5. Configure Feishu multi-account block

Ensure this shape exists in `~/.openclaw/openclaw.json`:

```json
{
  "channels": {
    "feishu": {
      "enabled": true,
      "defaultAccount": "default",
      "accounts": {
        "default": { "appId": "cli_xxx", "appSecret": "xxx", "enabled": true },
        "backup": { "appId": "cli_yyy", "appSecret": "yyy", "enabled": true }
      }
    }
  }
}
```

Never echo secrets back to users in plaintext.

### 6. Bind account to agent deterministically

Use one binding per account:

```json
{
  "bindings": [
    { "agentId": "main", "match": { "channel": "feishu", "accountId": "default" } },
    { "agentId": "assistant", "match": { "channel": "feishu", "accountId": "backup" } }
  ]
}
```

Or use CLI for simple cases:

```bash
openclaw agents bind --agent main --bind feishu:default
openclaw agents bind --agent assistant --bind feishu:backup
```

### 7. Ensure prompts are truly different

Update the non-main workspace files so system prompts diverge:

- `AGENTS.md`
- `SOUL.md`
- `IDENTITY.md`
- `USER.md`

Remove stale bootstrap template when persona setup is complete:

- `BOOTSTRAP.md`

### 8. Harden memory embeddings per new agent

Probe memory first:

```bash
openclaw memory status --agent assistant --deep --json
```

If `provider` is `none`, `embeddingProbe.ok=false`, or logs show provider errors, pin a working provider explicitly.

Example: route memory embeddings through OpenRouter OpenAI-compatible endpoint for `work-agent`:

```bash
AGENT_ID="work-agent"
IDX=$(openclaw agents list --bindings --json | jq -r --arg id "$AGENT_ID" 'to_entries[] | select(.value.id==$id) | .key')
KEY=$(jq -r '.profiles["openrouter:default"].key' ~/.openclaw/agents/$AGENT_ID/agent/auth-profiles.json)

openclaw config set "agents.list[$IDX].memorySearch.provider" '"openai"' --strict-json
openclaw config set "agents.list[$IDX].memorySearch.model" '"text-embedding-3-small"' --strict-json
openclaw config set "agents.list[$IDX].memorySearch.remote.baseUrl" '"https://openrouter.ai/api/v1"' --strict-json
openclaw config set "agents.list[$IDX].memorySearch.remote.apiKey" "\"$KEY\"" --strict-json
openclaw config set "agents.list[$IDX].memorySearch.fallback" '"none"' --strict-json
```

Then force index once:

```bash
openclaw memory index --agent work-agent --force --verbose
openclaw memory status --agent work-agent --deep --json
```

Expect:

- `provider` is not `none`
- `embeddingProbe.ok=true`
- `files/chunks` increase after indexing

### 9. Validate and restart

```bash
openclaw config validate
openclaw gateway restart
openclaw gateway status
openclaw channels status --probe
```

### 10. Prove routing with log evidence

Ask user to send `route-check` to each bot.
Then inspect logs:

```bash
openclaw channels logs --lines 300 | rg "feishu\\[(default|backup)\\].*dispatching to agent"
```

Expect:

- `feishu[default]` -> `session=agent:main:...`
- `feishu[backup]` -> `session=agent:assistant:...`

### 11. Approve pairing with explicit account

Always approve Feishu pairing with account scope in multi-account setups:

```bash
openclaw pairing list feishu --json
openclaw pairing approve feishu <code> --account <accountId> --notify
```

This prevents approving the same sender into the wrong account allowlist.

### 12. Handle common Feishu errors

`open_id cross app`:
- Cause: target open_id belongs to a different app account.
- Fix: send via matching `--account`, keep allowFrom scoped per account.
- Queue cleanup: archive stale cross-app deliveries in `~/.openclaw/delivery-queue/` before restart if they keep retrying.

`gemini embeddings failed: ... User location is not supported`:
- Cause: memory embedding provider resolves to Gemini in unsupported region.
- Fix: set per-agent `memorySearch.provider` to a supported provider/endpoint (example above).

`providerUnavailableReason` / `provider=none` in `openclaw memory status --deep`:
- Cause: no usable memory embedding credentials for that agent.
- Fix: configure agent-specific `memorySearch` provider + key, then run `openclaw memory index --agent <id> --force`.

`99991672` contact scope warning:
- Platform fix: grant one contact read scope in Feishu app.
- Config fallback: set `channels.feishu.resolveSenderNames=false`.

`cardkit:card:write` streaming error:
- Platform fix: grant `cardkit:card:write`.
- Config fallback: set `channels.feishu.streaming=false` and `channels.feishu.blockStreaming=false`.

## Output Contract

When finishing, report:

1. What changed (files + key fields).
2. Validation outputs (`config validate`, `gateway status`, `channels status --probe`).
3. Routing evidence lines for both accounts.
4. Memory evidence (`memory status --agent <id> --deep`, index result, provider/embedding probe state).
5. Any residual warnings and whether they are blocking.
