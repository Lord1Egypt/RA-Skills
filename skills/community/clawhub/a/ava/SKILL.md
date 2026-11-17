---
name: ava
description: >
  Lend real USDC on Base from your coding agent, inside limits the human sets.
  Ava handles session, mandate, two-phase preview, execution, and returns a
  receipt with chain proof. The agent never holds a key. Works from Claude
  Code, Cursor, Codex, and OpenClaw over HTTP MCP (https://www.getava.xyz/mcp).
  Fastest connect for Claude Code, Cursor, or Codex: npx @getava-xyz/connect.
  Live money is ava_lend_execute on Base (Morpho); copilot tools are testnet
  only. Use when: (1) the human wants their agent to allocate capital under
  bounds they set, (2) they ask for DeFi yield from a coding session, (3) they
  want a recomputable track record of agent executions. Triggers: Ava, agentic
  finance, MCP trading, mandate, agent wallet, OpenClaw DeFi, Claude trade,
  Cursor finance tools.
metadata:
  openclaw:
    requires:
      env: []
      optionalEnv:
        - AVA_API_BASE
        - AVA_USER_ID
        - AVA_TOKEN
        - AVA_PORTAL
        - AVA_ENABLE_LIVE
    primaryEnv: AVA_API_BASE
    homepage: https://getava.xyz
    tags:
      - defi
      - agentic-finance
      - trading
      - mcp
      - openclaw
      - multi-chain
      - mandates
---

# Ava

Ava lets a coding agent move real money without ever holding a key. The human
sets a mandate: asset, chain, cap. The agent works inside it. Every live
execution is two-phase: preview first, explicit human yes, then the same
`previewHash` executes. The receipt proves the fill on chain or says plainly
that it is unconfirmed.

Live today: USDC lending on Base via Morpho Blue, plus Aave v3 on Monad, BNB,
and Avalanche. One session, one bearer token, HTTP MCP.

## Why install this

- The agent never sees a private key. Signing happens server side behind policy.
- A mandate is a hard cap, not a suggestion. Exceeding it returns a typed
  refusal such as `MANDATE_NOTIONAL_EXCEEDED`.
- Receipts state what they can prove. `proof.standing: chain-confirmed` means
  the fill is on chain. Ava never writes a receipt for a fill it cannot show.
- A free testnet loop is included for rehearsal. It is labeled testnet and is
  never presented as live.

You (Claude / Cursor / OpenClaw) are one agent under a human `userId`. You
never invent a fill. Always call `tools/list` on the live server. Adapters are
internal settlement engines; never ask the human to pick a venue.

## Install

```bash
openclaw skills install @kamalbuilds/ava
```

Do not install from a path inside the private Ava repo. ClawHub is the public
pack: `@kamalbuilds/ava`.

Claude Code / Cursor / Codex, one command (not this OpenClaw pack):

```bash
npx @getava-xyz/connect
```

That writes HTTP MCP config after `ava_session`. Or add MCP yourself after `ava_session`:

```json
{
  "mcpServers": {
    "ava": {
      "type": "http",
      "url": "https://www.getava.xyz/mcp",
      "headers": { "Authorization": "Bearer ava_st_YOUR_TOKEN" }
    }
  }
}
```

Local: `http://127.0.0.1:8787/mcp`

## Hard rules

1. **Live money is `ava_lend_execute` on Base (Morpho).** Never use
   `ava_copilot_turn`, `ava_preview_tx`, or `ava_approve_execute` for live or
   mainnet funds.
2. **Session first, and keep the token.** Call `ava_session` once. Send the
   token as `Authorization: Bearer <token>` on every later call. A `userId` in
   tool arguments is a claim that must match the token.
3. **Default portal is Base.** Do not demo Sui. Do not swap USDC to SUI.
4. **`ava_create_mandate` is an Ava row, not user EIP-712 consent.** Say that.
5. **`ava_plan_standing` returns an unsigned envelope.** There is no MCP
   authorize or revoke. Do not claim hourly rotation is live.
6. **Copilot / `preview_tx` / `approve_execute` are testnet only.**
   `ava_portfolio` is seeded simulation. Never narrate them as live fills.
7. **Fail closed.** Typed refusal codes are success of the gate. The LLM is
   not the signer, policy, or verifier.

## Environment

```bash
# Defaults: AVA_API_BASE=https://api.getava.xyz, AVA_PORTAL=base.
# Local dev only: export AVA_API_BASE=http://127.0.0.1:8787
# AVA_USER_ID and AVA_TOKEN come from ava_session and are written to
# ~/.config/ava-openclaw/state.json (mode 0600). Never echo the token.
```

Local API: `http://127.0.0.1:8787`

## Two loops

| Loop | Tools | What it is |
|------|-------|------------|
| Live lend | `ava_session` → `ava_create_mandate` → `ava_lend_execute` | Morpho Blue on Base. Two-phase `previewHash`. |
| Testnet (not live) | `ava_copilot_turn` → `ava_preview_tx` → `ava_approve_execute` | Simulated quote. Not a live path. |

If the user wants real DeFi, use the live lend loop. Copilot is not a fallback
and not a rehearsal of `ava_lend_execute`.

## Live lend SOP (Mode A)

```text
1. ava_session                                              → userId + bearer token
2. connect https://www.getava.xyz/mcp with Authorization: Bearer
3. ava_create_mandate { portal: base, lend-only USDC }      → mandateId (unsigned Ava row)
4. ava_lend_execute without previewHash                     → preview artifact + hash
5. show preview; wait for explicit human yes
6. ava_lend_execute with the same mandateId + previewHash
7. return receipt. Success is proof.standing: chain-confirmed
```

Never retry after an ambiguous sign or submit. A new `executionId` is a new
economic action. Stop on `LEND_INSUFFICIENT_BALANCE`.

### Example

User: "Lend 100 USDC on Base with Morpho, under a tight mandate."

```text
ava_session
→ connect https://www.getava.xyz/mcp with Bearer token
→ ava_create_mandate (portal: base, lend-only USDC on Morpho)
→ ava_lend_execute (no previewHash) → show preview, wait for yes
→ ava_lend_execute (same mandateId + previewHash)
→ receipt with proof.standing: chain-confirmed
```

`verified: true` with unconfirmed standing is not a fill. `ok: true` with
`filled: false` is not a fill.

## CLI

```bash
node scripts/ava.mjs health
node scripts/ava.mjs session
node scripts/ava.mjs tools
node scripts/ava.mjs call ava_create_mandate '{"portal":"base","message":"Earn on 500 USDC on Base, max 5% drawdown"}'
node scripts/ava.mjs lend <mandateId>
# show preview to the human, then:
node scripts/ava.mjs lend <mandateId> <previewHash>
node scripts/ava.mjs portfolio
```

Testnet-only (not live capital):

```bash
node scripts/ava.mjs turn "Swap 10 USDC to WETH on base with 50 bps slip"
node scripts/ava.mjs approve <executionId>
```

## Proven venues

Re-check with `tools/list` on the live server. Proven: Morpho Blue on Base,
Aave v3 on Monad / BNB / Avalanche. Do not list CoW, Jupiter, Cetus,
Hyperliquid, Pendle, or Euler as live.

## Docs

- `docs/MCP.md`: protocol; `tools/list` is truth
- `docs/AGENTS.md`: coding-agent connect
- `research/progress/AGENTS_ARE_THE_USERS.md`: positioning lock
