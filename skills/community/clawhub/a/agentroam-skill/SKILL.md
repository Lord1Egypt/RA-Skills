---
name: agentroam-travel-connectivity
description: Buy travel eSIM data plans, gift cards, and mobile airtime with crypto (USDC, USDT, BTC, ETH, SOL and 17+ more) through AgentRoam. Use when a user wants an eSIM for a trip, a travel or brand gift card, or to top up a prepaid mobile number — paid from their own wallet, delivered by email. Trigger on "eSIM for <country>", "data plan for my trip", "buy a <brand> gift card with crypto", "top up a <carrier> number", "pay with USDC/USDT/BTC".
---

# AgentRoam — travel connectivity for humans and AI agents

AgentRoam sells three things, all paid with stablecoins and crypto straight from the
user's own wallet:

- **eSIM data plans** — 110+ countries and regions, plus Europe and Global multi-country plans. Instant QR by email.
- **Travel & brand gift cards** — Airbnb, Uber, airlines and 500+ US brands.
- **Mobile top-ups** — prepaid carriers in 100+ countries.

Purchases are fulfilled by **Cryptorefills B.V.** as merchant of record. AgentRoam never
holds funds or documents. Codes and eSIM QR codes are delivered by email, never through
the API.

## Connect

MCP server — Streamable HTTP, no authentication:

```
https://agentroam.ai/api/mcp
```

| Client | How |
| --- | --- |
| Claude Code | `claude mcp add --transport http agentroam https://agentroam.ai/api/mcp` |
| Claude.ai / Desktop | Add a remote MCP server, URL above |
| ChatGPT (developer mode) | Settings → Apps → Add MCP server, URL above |
| Any MCP client | Point a Streamable HTTP transport at the URL above |

Discovery manifest: `https://agentroam.ai/.well-known/mcp.json`

## Tools

| Tool | Use it to | Read-only |
| --- | --- | --- |
| `search_products` | Find gift cards, eSIM destinations, and top-up carriers by name | yes |
| `list_esim_plans` | Get live eSIM plans for a destination (renders a purchase widget in ChatGPT) | yes |
| `list_brands` | Browse all brands/carriers for a country | yes |
| `list_products` | List a brand's live denominations with crypto prices | yes |
| `get_price` | Live crypto quote for one product in any supported coin | yes |
| `get_currencies` | Supported payment coins (21) | yes |
| `get_payment_methods` | Full coin × network matrix (64 combos) | yes |
| `validate_order` | Dry-run an order → summary + one-time confirm token (10-min TTL) | no (local draft only) |
| `create_order` | Create the real order → wallet address, exact amount, QR, status URL | **no — spends money** |
| `get_order_status` | Track payment and delivery of an existing order | yes |
| `purchase_wizard` | Text-only step-by-step purchase flow for clients without widgets | no |

## Decision rules

| The user wants… | Use |
| --- | --- |
| An eSIM for a country/region | `list_esim_plans` (destination = ISO code, or `eu` / `ww`) |
| A specific brand's gift-card options | `list_products` (get the slug from `search_products` first) |
| To top up a phone abroad | `search_products` or `list_brands` with the country, then `list_products` |
| "How much does X cost in <coin>?" | `get_price` |
| "Which coins can I pay with?" | `get_payment_methods` |
| To actually buy something | `validate_order` → show summary → `create_order` (see gate below) |
| To check an order they already placed | `get_order_status` (needs the status token) |

## The confirm gate — REQUIRED before any purchase

1. Call `validate_order`. It mints a **local draft only** (no real order, no funds moved) and returns a human-readable summary plus a one-time `confirm_token` valid for 10 minutes.
2. **Show the summary to the user and get explicit approval.**
3. Only then call `create_order` with that token. It returns a wallet address, exact amount, network, QR, and a status URL. The user sends payment **from their own wallet**; the code/QR is emailed after payment confirms.

Never call `create_order` from exploration or without user approval — it creates a real
order with a 30-minute payment window.

## Do not

- **Do not book flights or hotels.** AgentRoam is connectivity + gift cards, not an online travel agency. (For stays, cross-link to MoodTrip; for flights, to Adin Flights.)
- **Do not give crypto prices, trading signals, or investment advice.** Crypto here is only a payment method.
- **Do not try to read or manage an eSIM already installed on the user's device** — AgentRoam sells new eSIMs, it has no access to the user's device or carrier account.
- **Do not invent** products, prices, coverage, or order states. Always use the tools; prices are live and change.

## Notes

- Coverage: 110+ eSIM destinations; gift cards are US-only today; top-ups span 100+ countries.
- Coins: USDC, USDT, BTC (incl. Lightning), ETH, SOL up front — 21 coins across 17 networks total.
- Verification (KYC) is only requested by the merchant of record above regulatory limits, and is handled on Cryptorefills' own pages — AgentRoam never sees documents.
