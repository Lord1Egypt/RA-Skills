---
name: clashofcoins-universal
description: Use when an agent needs one universal entrypoint to discover and use the unified Clash of Coins gateway (sale + shop), choose the active protocol on the live instance (x402 or mpp), and execute purchase or integration flows without mixing sale and shop contracts.
compatibility: Requires Node.js 18+ to run scripts/discover-gateway.mjs and outbound HTTPS access to the target gateway origin. Works in Agent Skills-compatible clients that can read SKILL.md and run shell commands.
---

# Clash of Coins Universal Skill

Use this as the default skill for any compatible agent (OpenClaw, Claude, Cursor, Codex, and other Agent Skills clients) when the task touches Clash of Coins.

Canonical published path: `/skills/clashofcoins-universal/SKILL.md`  
Compatibility aliases: `/skills/SKILL.md`, `/skills/clashofcoins-universal/skill.md`, `/skills/clashofcoins-universal`, `/skills/clashofcoins/SKILL.md`, `/skills/clashofcoins/skill.md`, `/skills/clashofcoins`

## Scope

- Surfaces: sale (`/agentic/*`) and shop (`/shop/*`)
- Protocol model: deployment-dependent (`x402`, `mpp`, or mixed)
- Role: universal router and discovery-first entrypoint

## Functional Coverage (Sale + Shop)

- Root discovery and routing:
  - `GET /`
  - `GET /openapi.json`
  - `GET /openapi.full.json`
  - `GET /mcp.json`
  - `GET /skills/index.json`
  - `GET /catalog`
  - check top-level `x-bazaar` metadata in OpenAPI for minimal Bazaar-compatible payable hints
  - `GET /.well-known/x402` (compatibility metadata for enabled x402 resources; `404` when x402 is disabled)
  - `GET /.well-known/mpp` when MPP is enabled
- Sale checkout coverage:
  - offers, optional quote, buy, and purchase-status polling on `/agentic/<protocol>/*`
  - request body constraints: `saleId`, `quantity`, `beneficiary`
- Shop checkout coverage:
  - anonymous + recipient-scoped catalog reads on `/shop/api/shop/items`
  - offers, optional quote, buy, and purchase-status polling on `/shop/<protocol>/*`
  - recipient constraint: exactly one of `nickname` or `address` for quote/buy
- Payment retry coverage:
  - x402 paid retry from latest challenge with identical method/body
  - MPP paid retry with identical JSON body and canonical `mppx` flow
- Agent-wallet coverage (when enabled):
  - read live capability/funding route first: `GET /agent-wallet/`
  - create order (returns exact amount): `POST /agent-wallet/orders`
  - payable funding (default auto sweep + finalize): `POST /agent-wallet/<fundingProtocol>/fund`
  - read order state: `GET /agent-wallet/orders/{orderId}`
  - funding status: `GET /agent-wallet/<fundingProtocol>/purchases/{paymentReference}`
  - funding protocol is runtime/env-driven (`x402` or `mpp`); purchase protocol in order payload can still be `x402` or `mpp` when enabled
- Integration coverage:
  - MCP/skills/OpenAPI consistency checks
  - scanner/registry validation via reference playbooks

## Use This Skill When

- user intent is not yet narrowed to sale or shop
- you need one playbook to browse, route, and execute
- you need to hand off cleanly to specialized skills after routing

## Do Not Use This Skill When

- task is explicitly sale-only and already scoped
- task is explicitly shop-only and already scoped

## Default Workflow

1. Pick one target origin. Do not mix origins in one pass.
2. Run discovery snapshot:
   - `node scripts/discover-gateway.mjs --origin <https://...>`
3. Read `GET /catalog` before any buy call.
4. Route by user intent:
   - browse/compare products: stay in this skill and follow `references/discovery-and-routing.md`
   - buy presale/NFT lots: follow sale flow in `references/purchase-playbooks.md`
   - buy in-game shop goods: follow shop flow in `references/purchase-playbooks.md`
   - scanner/MCP/OpenAPI integration or validation: use `references/integration-playbook.md`
5. Validate before execution:
   - active protocol exists on this origin
   - chosen surface matches the item (`sale` vs `shop`)
   - shop recipient rule is satisfied (exactly one of `nickname` or `address`)

## Hard Rules

- Do not mix sale and shop contracts in one purchase attempt.
- Do not treat payment settlement as success before purchase-status/ledger confirmation.
- Do not buy shop items from anonymous offers without recipient-scoped validation.
- Keep unpaid and paid retry payloads identical.
- Do not hardcode payment addresses or token/network constants outside deployment config.

## Fast Defaults

- Browse everything: `GET /catalog`
- Sale buy: `POST /agentic/<protocol>/buy`
- Shop buy: `POST /shop/<protocol>/buy`
- Agent-wallet buy flow:
  - `GET /agent-wallet/`
  - `POST /agent-wallet/orders`
  - `POST /agent-wallet/<fundingProtocol>/fund`
  - `GET /agent-wallet/orders/{orderId}`
- Sale status: `GET /agentic/<protocol>/purchases/{paymentTx}`
- Shop status:
  - `GET /shop/<protocol>/purchases/{paymentReference}`
  - `GET /shop/purchase-status/{purchaseId}` (user-facing status)

## Plan-Validate-Execute Loop

1. Plan: choose one origin, one surface, and one protocol from live discovery.
2. Validate: run the relevant checklist from references.
3. Execute: quote or buy.
4. Re-validate: if contract behavior differs, re-read live discovery and adjust.

## Agent Wallet Simplified Flow

1. Create order with purchase intent.
   - Read `GET /agent-wallet/` and use returned `fundingProtocol`/`fundingRoute` as source of truth.
   - `protocol` is optional; gateway can infer a compatible protocol (for example, shop carts prefer `mpp` when available).
2. Pay the funding route for returned `orderId`.
3. Expect backend to auto-run sweep and finalize.
4. Read order; if auto-execution fails, use manual recovery endpoints only as fallback.

## Load References On Demand

- Discovery and routing: `references/discovery-and-routing.md`
- Purchase playbooks: `references/purchase-playbooks.md`
- Integration/validator flow: `references/integration-playbook.md`
- Client setup: `references/client-installation.md`
- Skill eval artifacts:
  - quality evals: `evals/evals.json`
  - trigger evals: `evals/trigger-queries.json`

## Output Template

```markdown
### Clash of Coins Handoff

- Origin: <origin>
- Enabled protocols: <x402|mpp|both>
- Surface selected: <sale|shop>
- Why this route: <user intent + catalog evidence>
- Next endpoint: <method + path>
- Payload constraints: <recipient/beneficiary/cart rules>
- Payment retry rule: <PAYMENT-SIGNATURE or Authorization: Payment via mppx>
- Status endpoint: <exact path>
- Risks/gotchas: <if any>
```
