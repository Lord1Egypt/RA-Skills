---
name: a2a-market-acp-lite-negotiation
description: Gateway-only ACP negotiation skill with optional OpenClaw model-driven turn decisions.
---

# a2a-Market ACP Lite Negotiation

This skill is now **gateway-only**.
Single-turn local decision mode has been removed.

## Gateway Loop Mode (only mode)

Start one participant in one terminal:

```bash
node src/cli/index.js --role buyer --agent-id buyer-openclaw --gateway http://127.0.0.1:3085
```

Flow:
1. `POST /agents/register`
2. Loop `GET /agents/pull`
3. `POST /agents/respond`
4. For `NEGOTIATION_TURN`, decide by selected engine (`rule` or `openclaw`)

### Core flags

- `--role buyer|seller`
- `--gateway` (default `http://127.0.0.1:3085`)
- `--agent-id`
- `--decision-engine rule|openclaw` (default `rule`)
- `--auth-token` (default `market-auth-token`)
- `--pull-timeout-ms` (default `25000`)
- `--retry-delay-ms` (default `1000`)
- `--max-polls` (`0` means infinite)
- `--verbose true|false`

### OpenClaw engine flags

- `--provider-env` (default `OPENAI_API_KEY`)
- `--api-key` (optional direct key)
- `--allow-no-key true|false` (default `false`)
- `--thinking` (default `low`)
- `--timeout` seconds (default `60`)
- `--openclaw-extra-prompt` (optional)

### Auto-start session flags

- `--start-session true|false`
- `--counterparty-agent-id` (required with `--start-session true`)
- `--list-amount-minor-units` (default `9000`)
- `--currency` (default `USD`)
- `--max-rounds` (default `5`)
- `--product` (optional)
- `--goal` (optional)
- `--floor-minor-units` (optional)
- `--ceiling-minor-units` (optional)
- `--session-id` (default `nego_<timestamp>`)
- `--wait-counterparty-ms` (default `15000`)
- `--stop-on-session-end true|false`

## Single terminal: run skill + model + auto-kickoff

```bash
node src/cli/index.js \
  --role buyer \
  --agent-id buyer-openclaw \
  --gateway http://127.0.0.1:3085 \
  --decision-engine openclaw \
  --start-session true \
  --counterparty-agent-id seller-openclaw \
  --list-amount-minor-units 9000 \
  --currency USD \
  --max-rounds 5 \
  --wait-counterparty-ms 30000
```

## Executable Entrypoint

```bash
node src/cli/index.js
```
