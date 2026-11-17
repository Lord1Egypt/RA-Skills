# @ava/openclaw-skill

OpenClaw skill-pack for Ava, the accountability layer for agent-managed capital.

**Live loop:** session → list venues → mandate → `ava_lend_execute` two-phase
`previewHash` → receipt whose `proof.standing` is `chain-confirmed`.

**Testnet loop:** `ava_copilot_turn` → `ava_approve_execute`. Not live capital.

Same tools as Ava's HTTP MCP (`https://www.getava.xyz/mcp`). Testnet by default
for copilot quotes. Live lend is fail closed, and Ava never writes a receipt
for a fill it cannot show.

The word "paper" is deliberately absent. There is no paper mode on a blockchain.

## Why this exists

Distribution for crypto agents in 2026 is **OpenClaw skills + MCP**, not portal
matrices. Install the public pack; do not point OpenClaw at a path inside the
private Ava repo.

## Install

```bash
openclaw skills install @kamalbuilds/ava
```

Also documented on ClawHub as `npx skills add @kamalbuilds/ava`.

Claude, Cursor, and Codex (not this OpenClaw pack) use the public connect CLI:

```bash
npx @getava-xyz/connect
```

Then:

```bash
export AVA_API_BASE=https://api.getava.xyz
export AVA_PORTAL=base
node scripts/ava.mjs health
node scripts/ava.mjs session
node scripts/ava.mjs call ava_create_mandate '{"portal":"base","message":"Earn on 500 USDC on Base, max 5% drawdown"}'
node scripts/ava.mjs lend <mandateId>
# human confirms the preview
node scripts/ava.mjs lend <mandateId> <previewHash>
```

Local API: `AVA_API_BASE=http://127.0.0.1:8787`.

## Files

| File | Role |
|------|------|
| `SKILL.md` | Agent instructions (SOP, rules, tools) |
| `scripts/ava.mjs` | Zero-dep CLI over MCP/REST |
| `catalog.json` | Marketplace-style metadata |
| `.env.example` | Local env template |

## MCP tools used

- `ava_session`, `ava_create_mandate`, `ava_list_mandates`
- `ava_lend_execute` (live, two-phase `previewHash`)
- `ava_get_receipt`
- `ava_copilot_turn` / `ava_approve_execute` (testnet only)
- `ava_portfolio` (seeded simulation)

Docs: `../../docs/MCP.md`.

## Tests

```bash
node --test ./scripts/ava.test.mjs
```
