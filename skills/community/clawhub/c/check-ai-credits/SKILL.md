---
name: check-ai-credits
description: Check AI provider credits and balance across 10 services.
license: MIT
metadata:
  hermes:
    category: devops
    tags: [credits, balance, provider, usage, quota, cli]
---

# check-ai-credits

Use when the user asks how much credit/balance/quota is left on an AI
provider (DeepSeek, DeepInfra, Codex, Grok, MiMo, Claude, Gemini, Kimi,
OpenRouter, apikey.fun) — or "还剩多少钱 / 查额度 / 查余额".

## Commands

```bash
check-ai-credits                  # all configured providers
check-ai-credits <provider>       # one: deepseek|deepinfra|codex|grok|mimo|claude|gemini|kimi|openrouter|apikeyfun
check-ai-credits --json           # machine-readable snapshots
check-ai-credits --trend          # burn rate + days-left from history
check-ai-credits --list           # credential detection status per provider
check-ai-credits deepinfra --models  # per-model month breakdown
```

Binary location: `dist/check-ai-credits` after `bun run build`, or run
directly with `bun src/cli.ts`.

## Output contract

`--json` returns the snapshot schema
(`provider, source, timestamp, currency, balance, usedPercent, resetsAt,
monthCost, monthPeriod, details, error`). Check `error` first; a non-null
`error` means the balance fields are unreliable. `authHint` carries the login
URL when credentials expired.

## Common failures

1. `DEEPSEEK_API_KEY missing` → key resolves from process env first, then
   `$HERMES_HOME/.env`; set it there, never hardcode.
2. `codex/grok auth token is expired` → run the vendor CLI once (`codex` /
   `grok login`); this tool never refreshes tokens itself because that would
   rotate the CLI's refresh token.
3. `codexbar … returned no data` → Claude/Gemini/Kimi/OpenRouter/apikeyfun
   need the CodexBar app installed; run `codexbar usage` once interactively.

## Safety

Read-only credential access, no secret echo in any output mode, no telemetry.
Do not edit provider files to "fix" a failure without checking the endpoint
semantics in `docs/MIGRATION.md` first (DeepInfra costs are in cents; Grok
units are credits, not dollars).
