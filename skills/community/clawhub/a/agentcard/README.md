
<p align="center">
  <a href="https://npmjs.com/package/@asgcard/sdk"><img src="https://img.shields.io/npm/v/@asgcard/sdk?label=sdk" alt="npm"></a>
  <a href="https://npmjs.com/package/@asgcard/cli"><img src="https://img.shields.io/npm/v/@asgcard/cli?label=cli" alt="cli"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License"></a>
  <a href="https://api.asgcard.dev/health"><img src="https://img.shields.io/badge/API-live-brightgreen" alt="API Status"></a>
  <a href="https://asgcard.dev/docs"><img src="https://img.shields.io/badge/Docs-asgcard.dev-blue" alt="Docs"></a>
</p>

<p align="center">
  <a href="#quick-start">Quick Start</a> ·
  <a href="https://asgcard.dev/docs">Docs</a> ·
  <a href="https://asgcard.dev">Website</a> ·
  <a href="https://x.com/asgcardx402">Twitter</a> ·
  <a href="SECURITY.md">Security</a>
</p>

---

> **Public mirror** — this repo is a read-only mirror of the internal monorepo.
> For issues and feature requests use [GitHub Issues](https://github.com/ASGCompute/asgcard-public/issues).
> For code contributions see [CONTRIBUTING.md](CONTRIBUTING.md).

# Agent Card

Agent Card is an **agent-first** virtual card platform. AI agents programmatically issue and manage MasterCard virtual cards, paying in USDC via the **x402** protocol on **Stellar**.

<div align="center">
<table>
  <tr>
    <td align="center"><strong>Works<br/>with</strong></td>
    <td align="center"><a href="https://openai.com/index/codex/"><img src=".github/assets/logos/codex.svg" width="32" alt="Codex" /></a><br/><sub>Codex</sub></td>
    <td align="center"><a href="https://claude.ai/code"><img src=".github/assets/logos/claude.svg" width="32" alt="Claude Code" /></a><br/><sub>Claude Code</sub></td>
    <td align="center"><a href="https://cursor.com"><img src=".github/assets/logos/cursor.svg" width="32" alt="Cursor" /></a><br/><sub>Cursor</sub></td>
    <td align="center"><a href="https://openclaw.ai"><img src=".github/assets/logos/openclaw.svg" width="32" alt="OpenClaw" /></a><br/><sub>OpenClaw</sub></td>
    <td align="center"><a href="https://modelcontextprotocol.io"><img src=".github/assets/logos/mcp.svg" width="32" alt="Any MCP Client" /></a><br/><sub>Any MCP</sub></td>
  </tr>
</table>

<table>
  <tr>
    <td align="center"><strong>Built<br/>with</strong></td>
    <td align="center"><a href="https://stellar.org"><img src=".github/assets/logos/stellar.svg" width="32" alt="Stellar" /></a><br/><sub>Stellar</sub></td>
    <td align="center"><a href="https://www.circle.com/usdc"><img src=".github/assets/logos/circle.svg" width="32" alt="Circle USDC" /></a><br/><sub>Circle USDC</sub></td>
    <td align="center"><a href="https://www.mastercard.com"><img src=".github/assets/logos/mastercard.svg" width="32" alt="MasterCard" /></a><br/><sub>MasterCard</sub></td>
  </tr>
</table>

<em>If it speaks MCP, it can spend.</em>

</div>

## 🎬 Demo

<p align="center">
  <img src=".github/assets/demo.gif" alt="Agent Card CLI Demo" width="600">
</p>

> 📹 [Watch the full product video](https://youtu.be/zEq3HGhwrY8)

## Agent Card is right for you if

- ✅ Your AI agent needs to **pay for things** — hosting, domains, APIs, SaaS
- ✅ You want a virtual MasterCard issued **programmatically**
- ✅ You want your agent to manage cards **autonomously via MCP**
- ✅ You want to pay in **USDC** without touching fiat banking
- ✅ You need transparent, **on-chain proof** of every payment

## Quick Start

### For Codex

```bash
npx @asgcard/cli onboard -y --client codex
```

### For Claude Code

```bash
npx @asgcard/cli onboard -y --client claude
```

### For Cursor

```bash
npx @asgcard/cli onboard -y --client cursor
```

### Using the SDK directly

```bash
npm install @asgcard/sdk
```

### Via ClawHub

```bash
npx clawhub@latest install agentcard
```

The onboarding flow creates a Stellar wallet (`~/.asgcard/wallet.json`), configures MCP, installs the agent skill, and prints the next step.

> **Note:** If you already have a wallet, run `npx @asgcard/cli doctor` to verify your setup.

## How It Works

1. **Agent requests a card** → API returns `402 Payment Required` with USDC amount
2. **Agent signs a Stellar USDC transfer** via the SDK
3. **x402 Facilitator verifies and settles** the payment on-chain
4. **API issues a real MasterCard** via the card issuer
5. **Card details returned** in the response

Live pricing: [`GET https://api.asgcard.dev/pricing`](https://api.asgcard.dev/pricing) · Full docs: [asgcard.dev/docs](https://asgcard.dev/docs)

## MCP Server (9 tools)

`@asgcard/mcp-server` exposes **9 tools** via the Model Context Protocol. The MCP server reads your Stellar key from `~/.asgcard/wallet.json` — **no env vars needed** in client configs.

| Tool | What it does |
|------|--------------|
| `get_wallet_status` | Wallet address, USDC balance, readiness |
| `create_card` | Create virtual MasterCard (x402 payment) |
| `fund_card` | Top up existing card |
| `list_cards` | List all wallet cards |
| `get_card` | Card summary |
| `get_card_details` | PAN, CVV, expiry (nonce-protected) |
| `freeze_card` / `unfreeze_card` | Freeze or re-enable a card |
| `get_pricing` | Current tier pricing |

## SDK

```typescript
import { ASGCardClient } from "@asgcard/sdk";

const client = new ASGCardClient({
  privateKey: "S...",  // Stellar secret key
  rpcUrl: "https://mainnet.sorobanrpc.com"
});

const card = await client.createCard({
  amount: 10,
  nameOnCard: "AI Agent",
  email: "agent@example.com"
});
```

See [`/sdk`](sdk/) for full API reference.

## Repository Structure

This is a monorepo. Most users should use **`npx @asgcard/cli`** or **`npm install @asgcard/sdk`** — cloning is only needed for contributing.

| Directory | Package |
|-----------|---------|
| `/api` | ASG Card API (Express + x402 + wallet auth) |
| `/sdk` | `@asgcard/sdk` — TypeScript client |
| `/cli` | `@asgcard/cli` — CLI + onboarding |
| `/mcp-server` | `@asgcard/mcp-server` — MCP server (9 tools) |
| `/web` | Marketing website (asgcard.dev) |
| `/docs` | Documentation and ADRs |

## Security

- 🔒 AES-256-GCM encryption at rest for card details
- 🔑 Stellar private key **never leaves your machine** (`~/.asgcard/wallet.json`)
- 🛡️ Nonce-based anti-replay protection
- ✅ Wallet signature authentication — no API keys
- 📋 [Security Policy](SECURITY.md) · [Technical Overview](TECHNICAL_OVERVIEW.md)

## Community

- [GitHub Issues](https://github.com/ASGCompute/asgcard-public/issues) — bugs and feature requests
- [asgcard.dev](https://asgcard.dev) — docs and website
- [Twitter/X](https://x.com/asgcardx402) — updates

## License

MIT © 2025 ASG Compute
