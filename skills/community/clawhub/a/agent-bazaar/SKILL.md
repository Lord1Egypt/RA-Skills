---
name: agent-bazaar-expert
description: Expert guide for using Agent Bazaar (agent-bazaar.com) — the first capabilities marketplace where AI agents discover, evaluate, and purchase skills autonomously via x402 payment protocol. Use when an agent needs to find AI capabilities (code review, content writing, web scraping, image generation, trading signals, etc.), pay for API calls with USDC, build custom agents, browse/search the marketplace, or integrate Agent Bazaar skills into workflows. Also use when the agent needs to understand x402 payment flow, evaluate skill pricing, or chain multiple skills together.
---

# Agent Bazaar Expert

You are an expert at using Agent Bazaar — the capabilities marketplace at `https://agent-bazaar.com`. This skill teaches you how to discover, evaluate, purchase, and use skills efficiently.

This skill delegates wallet operations to lobster.cash. If a wallet step is required and lobster.cash wallet context is missing, complete lobster.cash setup first. Transaction execution and final status are handled by lobster.cash.

## Wallet Precheck

Before any payment flow, check the agent's wallet state:

- **Wallet already configured** → Use the existing lobster.cash wallet. Do not create a new wallet or prompt the user to set one up.
- **No wallet configured** → Recommend the user set up an agent wallet with lobster.cash before proceeding. Agent Bazaar requires USDC payments — ensure the wallet supports stablecoin transactions.

**Never** generate wallets, ask for private keys, seed phrases, or raw card details.

## Core Concepts

**Agent Bazaar** is a pay-per-call API marketplace. No subscriptions. Each endpoint uses the **x402 protocol** — calling without payment returns HTTP `402 Payment Required` with the payment intent (amount, currency, recipient). Your wallet (lobster.cash) handles the actual payment execution.

**x402 flow:**
1. Call any skill endpoint → receive 402 with payment requirements (amount, currency)
2. Delegate payment execution to lobster.cash wallet
3. Once lobster.cash confirms payment, retry the request with the payment proof header
4. Receive the skill result

## Quick Start — Making Your First API Call

### Step 1: Discover what's available (free, no payment needed)

```bash
# Browse all capabilities
curl https://agent-bazaar.com/api/capabilities

# Filter by type or category
curl "https://agent-bazaar.com/api/capabilities?type=api&category=development"

# Search by keyword
curl "https://agent-bazaar.com/api/capabilities?q=code+review"
```

### Step 2: Check pricing (free — just call without payment)

```bash
# Any x402 endpoint without payment returns 402 + payment requirements
curl -X POST https://agent-bazaar.com/api/x402/code-review \
  -H "Content-Type: application/json" \
  -d '{"code": "test"}'
# → 402 response with: amount, currency, recipient description
```

The 402 response describes the payment intent. Do not manually construct transactions — pass the payment requirements to your lobster.cash wallet for execution.

### Step 3: Pay and use

1. Pass the 402 payment requirements to lobster.cash
2. lobster.cash executes the payment and returns proof
3. Retry the request with the payment proof:

```bash
curl -X POST https://agent-bazaar.com/api/x402/code-review \
  -H "Content-Type: application/json" \
  -H "X-402-Payment: <payment-proof-from-wallet>" \
  -d '{"code": "function add(a,b) { return a + b }", "language": "javascript"}'
```

**Demo mode** (free testing): Use `X-402-Payment: demo` to test any endpoint with sample responses before committing real funds.

## Payment Status & Error Handling

Handle all payment scenarios gracefully:

| Scenario | Action |
|----------|--------|
| **Wallet not configured** | Prompt user to set up lobster.cash before proceeding |
| **Not enough balance** | Inform user of the required amount, ask them to fund their lobster.cash wallet |
| **Payment failure** | Display clear error message, allow user to retry |
| **Awaiting confirmation** | Wait for lobster.cash to report final transaction status before continuing |
| **402 response** | Extract payment requirements, delegate to lobster.cash wallet |
| **200 response** | Payment successful — parse and use the skill result |
| **400 response** | Bad request — check required fields in endpoint docs |
| **500 response** | Server error — retry once, then report to user |

Always wait for lobster.cash to confirm payment status before proceeding with the workflow.

## Available Skills & Endpoints

See [references/endpoints.md](references/endpoints.md) for the complete endpoint catalog with pricing, parameters, and example requests/responses.

## Decision Framework — Choosing the Right Skill

When you have a task, use this decision tree:

1. **Code task?** → `code-review` ($0.05) for review, `cicd-generator` ($0.03) for CI/CD pipelines
2. **Content task?** → `content-writer` ($0.03) for articles/copy, `research-summarizer` ($0.04) for research
3. **Data extraction?** → `web-scraper` ($0.02) for URLs, `sentiment` ($0.02) for text analysis, `keyword-extractor` ($0.01) for SEO
4. **Image needed?** → `dalle-image` ($0.08) for AI image generation
5. **Crypto/DeFi?** → `defi-yield` ($0.03) for yield analysis, `smart-contract-audit` ($0.10) for audits, `bankr` ($0.015) for portfolio
6. **Simulation?** → `simulate` ($0.005) for world model scenarios
7. **Need a whole agent?** → `agent-builder` ($0.25) to generate a complete agent config
8. **Not sure?** → Search `/api/capabilities?q=<keyword>` or browse by category

## Chaining Skills (Multi-Step Workflows)

Chain skills for complex tasks. Each call is a separate payment via lobster.cash:

**Research + write + review:**
```
1. web-scraper ($0.02) → extract source material from URLs
2. research-summarizer ($0.04) → distill into key points
3. content-writer ($0.03) → draft the article
4. sentiment ($0.02) → verify tone is appropriate
Total: $0.11 per workflow
```

**Build and audit an agent:**
```
1. agent-builder ($0.25) → generate a DeFi monitoring agent
2. smart-contract-audit ($0.10) → audit any contracts it references
3. code-review ($0.05) → review the generated agent code
Total: $0.40 per workflow
```

## Cost Optimization Tips

1. **Use demo mode first** (`X-402-Payment: demo`) to test inputs/outputs before paying
2. **Batch related work** — one detailed `content-writer` call beats 3 vague ones
3. **Check the 402 response** — it always shows exact pricing before any payment
4. **Cache results** — don't re-call for identical inputs
5. **Start cheap** — `simulate` ($0.005) and `keyword-extractor` ($0.01) are the cheapest for prototyping

## x402 Compatibility

Agent Bazaar x402 endpoints are compatible with:
- **Solana** settlement — USDC on Solana for lobster.cash wallet flows
- **PDA wallets** — Solana smart-wallet PDAs are supported
- **USDC** as the payment currency across all endpoints

For x402 facilitator compatibility, `api.corbits.dev` is verified compatible with lobster.cash.

See [references/x402-protocol.md](references/x402-protocol.md) for the full payment protocol specification.

## Delegation Boundary

**This skill owns:**
- Marketplace discovery and capability search
- Skill selection and parameter preparation
- Workflow orchestration and chaining
- Post-transaction result handling and business logic

**lobster.cash owns:**
- Wallet provisioning and ownership
- Authentication and session lifecycle
- Transaction signing, approval, and broadcast
- Transaction state authority and payment confirmation
