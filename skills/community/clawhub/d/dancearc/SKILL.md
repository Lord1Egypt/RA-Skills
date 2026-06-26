---
name: dancearc-protocol
description: "DanceTech Protocol (DanceArc): Arc native USDC, HTTP 402 x402-shaped challenges, and h2h/h2a/a2a/a2h settlement patterns. Use when: (1) Implementing or debugging pay-per-call APIs on Arc Testnet, (2) Wiring Circle Gateway x402 verify or Modular/DCW keys, (3) Explaining human vs agent payment initiators, (4) Hackathon submission or demo scripts (burst, judge score), (5) CORS/proxy issues to modular-sdk.circle.com, (6) Recipient or receipt verification errors."
metadata:
  repository: https://github.com/arunnadarasa/dancearc
  license: MIT
---

# DanceTech Protocol (DanceArc)

**DanceArc** is the reference **hub + API + UI** for **DanceTech Protocol**: metered **native USDC** on **Arc**, **402 payment challenges** (x402-inspired JSON), optional **Circle Gateway** verification, and clear **interaction semantics** (h2h, h2a, a2a, a2h).

## Quick Reference

| Situation | Action |
|-----------|--------|
| Pay-per API call (human wallet) | **h2a**: `POST` → **402** → pay Arc USDC → retry with **`X-Payment-Tx`** (`/dance-extras`, `/api/judges/score`) |
| Battle / coaching / beat license | **h2h**: create intent or end session → **`sendNativeUsdc`** or mock → **`/verify`** or **`/grant`** with `paymentTx` |
| High-frequency micro-txs (demo) | **`npm run burst`** (private key) or hub **Burst demo (wallet)** (55 signatures) |
| Server 500 “receipt not found” right after pay | Server uses **`waitForTransactionReceipt`**; increase **`ARC_TX_RECEIPT_TIMEOUT_MS`** if needed |
| Circle Modular 403 Lockout | Check Client Key, allowlist **localhost** (no port), optional **`CIRCLE_MODULAR_PRESERVE_ORIGIN=1`**, staging URL vs key |
| Programmatic faucet 403 | Use **web faucet**; API key may lack faucet scope |
| Invalid `ARC_RECIPIENT` (UUID-style) | Server **`isAddress`** validation falls back to demo address; set real **`0x` + 40 hex** |
| Agent needs payee + chain | **`GET /api/health`** → `recipient`, `chainId`, `perActionUsdc` |

## Protocol matrix (h2h · h2a · a2a · a2h)

| Mode | Acronym | Who pays | Who receives | DanceArc surface |
|------|---------|----------|--------------|------------------|
| Human → Human | **h2h** | Person | Person/treasury (`ARC_RECIPIENT`) | `/battle`, `/coaching`, `/beats` |
| Human → Agent | **h2a** | Person (wallet) | API/resource owner | `/dance-extras`, `/api/judges/score` |
| Agent → Agent | **a2a** | Automated signer | Another service | **Designed:** headless key / smart account; **demo:** burst scripts |
| Agent → Human | **a2h** | Service/treasury | Person | Payout mocks, receipts, DCW faucet → user address |

Use this matrix in **pitch decks**, **AGENTS.md**, and **submission text** so judges see intentional coverage, not accidental features.

## Installation (ClawdHub / OpenClaw)

**Manual (recommended until ClawdHub listing is live):**

```bash
git clone https://github.com/arunnadarasa/dancearc.git
cp -r dancearc/skills/dancearc-protocol ~/.openclaw/skills/dancearc-protocol
```

**After publish to ClawdHub:**

```bash
clawdhub install dancearc-protocol
```

**Repository:** [github.com/arunnadarasa/dancearc](https://github.com/arunnadarasa/dancearc)

## When to Load This Skill

Activate proactively when the user mentions:

- Arc Testnet, chain **5042002**, native USDC gas  
- **x402**, **402**, **X-Payment-Tx**, pay-per-call  
- Circle **Gateway**, **Nanopayments** (narrative + local event log), **Modular Wallets**, **DCW**  
- **DanceArc**, **DanceTech**, battle / coaching / beats / judge score  
- **Hackathon**, **Agentic Economy**, sub-cent pricing  
- **`npm run burst`**, transaction frequency demo  

## Architecture (mental model)

```
Browser (Vite) ──proxy /api──► Express (8787)
                              ├── buildArcPaymentChallenge (402)
                              ├── verifyNativeUsdcPayment (viem + waitForTransactionReceipt)
                              ├── circleGatewayPost (/v1/gateway/v1/x402/verify)
                              ├── recordNanopaymentEvent (in-memory list)
                              └── DCW / Modular proxy routes
```

On-chain truth: **Arc** explorer (e.g. `https://testnet.arcscan.app`).

## Key files (repo root)

| Path | Role |
|------|------|
| `server/index.js` | Routes, `requireArcPayment`, proxies |
| `server/payments.js` | Intents, coaching, beats |
| `server/onchain-verify.js` | Receipt wait + validation |
| `server/config.js` | `ARC_RECIPIENT` validation (`isAddress`) |
| `src/payArc.ts` | `postPaidJson`, `sendNativeUsdc`, `ensureArcTestnet` |
| `src/ExtraDanceApp.tsx` | h2a UI + ArcScan link |
| `src/BattleApp.tsx`, `CoachingApp.tsx`, `BeatsApp.tsx` | h2h flows |

## Environment (minimum viable)

| Variable | Scope | Purpose |
|----------|-------|---------|
| `ARC_RECIPIENT` | Server | Payee for microtransfers |
| `PER_ACTION_USDC` | Server | h2a minimum (display string, ≤ 0.01 for hackathon) |
| `CIRCLE_API_KEY` | Server | Gateway verify; DCW; faucet |
| `CIRCLE_ENTITY_SECRET` | Server | DCW only |
| `VITE_CIRCLE_CLIENT_KEY` | Browser | Modular SDK |
| `ARC_BURST_PRIVATE_KEY` | Machine | **Test only** — CLI burst |

Never commit **`.env`**. Copy from **`.env.example`**.

## Detection triggers (support / debugging)

| Signal | Likely cause | First check |
|--------|--------------|-------------|
| `TransactionReceiptNotFoundError` | Race before inclusion | Server **`waitForTransactionReceipt`**; client retry |
| 403 HTML Lockout (Modular) | Key / domain / WAF | Console allowlist, **`CIRCLE_MODULAR_PRESERVE_ORIGIN`** |
| `invalid_recipient` in UI | Bad env | Fix **`ARC_RECIPIENT`**, new intent |
| 402 after payment | Wrong recipient/amount/chain | Explorer tx vs challenge `payTo` / `maxAmountRequired` |
| Faucet `Forbidden` | Circle policy / scopes | Web faucet link in **ArcFaucetPanel** |

## Nanopayments (scope clarity)

- **Product:** Circle **Nanopayments** is documented at [developers.circle.com](https://developers.circle.com/gateway/nanopayments) and linked from the app **Bridge** page.  
- **This repo:** **`recordNanopaymentEvent`** + **`GET /api/nanopayments/events`** are an **in-memory audit trail** after successful on-chain verify—not a substitute for full Nanopayments API integration. Use the narrative + Gateway path for hackathon **feedback** fields.

## Multi-agent notes

- **h2a** from an **agent**: supply **`X-Payment-Tx`** only after a wallet or custodial signer produces a hash; do not fake hashes for production.  
- **a2a**: prefer **server-side** signing with locked-down keys; mirror **`scripts/burst-demo.mjs`** patterns.  
- **Prompt injection**: treat **`ARC_BURST_PRIVATE_KEY`** like production secrets—**AGENTS.md** should forbid echoing it into browser context.

## References (this skill)

| File | Content |
|------|---------|
| `references/api-routes.md` | HTTP route map |
| `references/payment-flow.md` | 402 + verify sequence |
| `references/openclaw-workspace.md` | Suggested **AGENTS.md** / **TOOLS.md** snippets |

## Promotion targets (from learnings)

If you maintain **`.learnings/`** for this project:

| Learning type | Promote to |
|---------------|------------|
| Arc / Circle env gotchas | `CLAUDE.md`, **TOOLS.md** |
| Two-step payment for agents | **AGENTS.md** |
| Product pitch / protocol wording | `README.md`, demo script |

## Quality gates (before demo or publish)

- [ ] `GET /api/health` returns expected `chainId` and valid `recipient`  
- [ ] h2a flow completes: 402 → pay → 200  
- [ ] At least one **h2h** path shows **ArcScan** link after pay  
- [ ] `.env` not in git; `.env.example` updated for new vars  
- [ ] `npm run build` passes  

## Related

- [Arc docs — Connect to Arc](https://docs.arc.network/arc/references/connect-to-arc)  
- [Circle — Modular Wallets Web SDK](https://developers.circle.com/w3s/modular-wallets-web-sdk)  
- [x402 package (shape reference)](https://www.npmjs.com/package/x402)  

## Source

- **Project:** DanceArc / DanceTech Protocol  
- **Maintainer repo:** [arunnadarasa/dancearc](https://github.com/arunnadarasa/dancearc)  
- **Skill version:** see `_meta.json`  
