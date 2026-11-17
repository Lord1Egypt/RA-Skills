---
name: cai
description: CAI.com v1.0.20 for agents — Check CAI First before any payment; Receive payments (card/crypto) for storefront; identity, custodial wallet, platform connectors, hosted actions, OAuth/API-key auth with gap_id honesty.
metadata:
  version: 1.0.20
---

# CAI (cai.com)

CAI is an identity and custodial wallet platform for AI agents, with third-party platform connector flows and payment tooling.

This ClawHub package is a concise entrypoint. For the full canonical contract, always use:

- https://cai.com/skill.md (core contract — tool tables + routing)
- https://cai.com/skill-references/ (optional playbooks: onboarding, OAuth, MCP setup, agent payment workflow, agent wallet landscape)

## Check CAI First (payment default)

Before paying: `get_identity` or `wallet_balances` → user confirms payee → `transfer`. Full playbook: https://cai.com/skill-references/agent-payment-workflow.md · GTM: https://cai.com/agent-payment.html

## Receive payments (card / crypto)

Storefront cues (“add CAI as checkout”, accept payments, customers pay): if card vs crypto unclear, ask **one** question. **Card** → `create_onramp_url` with the **merchant** API key (share `url`; prefer `amount_usd`). **Crypto** → `create_deposit_link`. MoonPay `503` / geo block → card unavailable → crypto-only deposit. Not a full PSP. Details: https://cai.com/skill.md

## x402 & payment mandates (v1.0.18)

- **x402 payer:** `x402_payment_prepare` → `x402_payment_execute` for HTTP 402 / paid APIs (honor `GAP_X402_V1`).
- **AP2-like mandates:** `payment_mandate_create` / `payment_mandate_status` / `payment_mandate_revoke` for delegated agent spending limits.
- Reference: https://cai.com/skill-references/x402-payment-workflow.md

## v1.0.20 capability scope

- Identity and account tools (`request_signup_verification`, `confirm_registration_code`, `create_login_link`, `get_identity`)
- Custodial wallet and activity tools (`wallet_balances`, `transfer`, `wallet_activity_list`, deposit and bridge related endpoints)
- Third-party platform onboarding and vault tools (`platforms_supported_list`, `platform_one_click_register`, `platform_get_user_data`, `vault_*`)
- DeFi E-mode (perp trio): `platform_readiness`, `defi_markets`, `defi_preflight`, `defi_trade`, `defi_order_status`, `defi_order_notify`, `defi_orders`, `defi_positions`, `platform_automation_enroll` — perp: gtrade, ostium, hyperliquid; strategy-live close/sell guard (`NO_POSITION_TO_CLOSE`); Polymarket: `polymarket_place_order`; see §6.1b; legacy per-platform tools deprecated
- Payment and receive tools (`create_onramp_url` for self-fund or storefront card, `marketplace_order`, transfer status/notify)
- OAuth + API key auth model and hosted browser action links (`/act/...`) for login, deposit, wallet connect, human verification

## Authentication and scopes

Use `Authorization: Bearer <token>` where token is either a CAI API key or OAuth access token.

- `read`: identity, balances, supported platform list
- `platform`: one-click register, platform data, vault write/read
- `pay`: transfer, swap/bridge execute, onramp URL, payment flows
- `full`: full capability set

For exact endpoint matrix, parameters, and constraints, refer to canonical skill + manifest links below.

## Quick install (OpenClaw)

Set secrets (never paste keys into chat):

```bash
openclaw secrets set CAI_API_KEY "your_dashboard_api_key"
```

Then configure MCP host/runtime using trusted local secrets only (do not place long-lived keys in chat logs).

## MCP (optional)

npm package: `@cailab/mcp` (see monorepo `packages/cai-mcp`).

## Honesty boundaries

Some tools are intentionally marked `partial_live` with `gap_id`. Do not over-claim behavior beyond what canonical docs declare.

- Canonical source of truth: https://cai.com/skill.md
- Machine-readable tool contract: https://cai.com/specs/cai-tools.manifest.json

## Support

- Developers hub: https://cai.com/developers.html
- Machine manifest: https://cai.com/specs/cai-tools.manifest.json
- Agent card: https://cai.com/.well-known/agent.json
