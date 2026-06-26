# ⛽ Agent Fuel — Autonomous Agent Payment & Gas Management

> When agents run out of gas, they refuel themselves. No human required.

**Tracks:** MoonPay CLI Agents · OpenWallet Standard · Agent Services on Base  
**Event:** Synthesis Hackathon (March 2026)  
**Builder:** @Zedit42 + Xeonen (AI Agent, OpenClaw)

---

## 🎯 The Problem

AI agents need to transact onchain — pay for API calls, execute trades, deploy contracts. But when their wallet runs dry:

- ❌ Agent stops working
- ❌ Human has to manually top up
- ❌ Tasks fail silently
- ❌ Autonomous loops break

Every "autonomous" agent has a single point of failure: **an empty wallet.**

## 💡 The Solution

**Agent Fuel** is an OpenClaw skill that gives any AI agent autonomous financial self-sufficiency:

```
Agent needs gas → checks balance → low? → MoonPay CLI buys crypto → agent continues
                                                    ↑
                                   x402 payment for API calls ←→ auto-settle
```

### How It Works

1. **Balance Monitoring** — Agent watches its wallet balance across any chain (EVM, Solana)
2. **Auto Top-Up via MoonPay** — When balance drops below threshold, MoonPay CLI triggers a purchase (fiat→crypto or swap)
3. **x402 Native Payments** — For API calls that support x402, agent pays per-request automatically. No API keys, no subscriptions.
4. **OpenWallet Standard** — Chain-agnostic wallet management. Works with any EVM chain, Solana, or L2.
5. **Spending Limits** — Human sets max spend per day/week. Agent can't exceed it.

### Architecture

```
┌─────────────────────────────────────────────────┐
│              AI AGENT (OpenClaw)                 │
│                                                   │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐      │
│  │ Balance   │  │ x402     │  │ Spending │      │
│  │ Monitor   │  │ Client   │  │ Limiter  │      │
│  └─────┬────┘  └─────┬────┘  └─────┬────┘      │
│        │             │             │              │
│  ┌─────▼─────────────▼─────────────▼────┐       │
│  │        OpenWallet Standard            │       │
│  │   (chain-agnostic wallet layer)       │       │
│  └─────────────────┬────────────────────┘       │
│                    │                              │
└────────────────────┼──────────────────────────────┘
                     │
         ┌───────────┼───────────┐
         │           │           │
    ┌────▼───┐  ┌────▼───┐  ┌───▼────┐
    │MoonPay │  │  x402  │  │  Any   │
    │  CLI   │  │Facilit.│  │ Chain  │
    │(top-up)│  │(settle)│  │(tx/gas)│
    └────────┘  └────────┘  └────────┘
```

## 🔧 Installation

```bash
# Install as OpenClaw skill
clawhub install agent-fuel

# Or manually
npm install -g @moonpay/cli
mp login
```

## 📋 Configuration

```json
{
  "wallet": {
    "chain": "base",
    "minBalance": "5.00",
    "topUpAmount": "20.00",
    "currency": "USDC"
  },
  "moonpay": {
    "autoTopUp": true,
    "maxDailySpend": "100.00",
    "fundingSource": "card"
  },
  "x402": {
    "enabled": true,
    "maxPerRequest": "0.10",
    "facilitator": "https://x402.org/facilitator"
  }
}
```

## 🚀 Usage

### As an OpenClaw Skill

```
Agent: "I need to call the premium API but my wallet is low."
Agent Fuel: Checking balance... $2.30 USDC (below $5 threshold)
Agent Fuel: Triggering MoonPay top-up... buying $20 USDC
Agent Fuel: ✅ Balance now $22.30 USDC. Resuming operations.
```

### x402 Auto-Pay

```
Agent → GET https://api.example.com/data
Server → 402 Payment Required (0.001 USDC)
Agent Fuel → Signs payment, retries request
Server → 200 OK + data
```

### CLI Commands

```bash
# Check agent wallet balance
mp wallet balance

# Manual top-up
mp buy --amount 20 --currency USDC --chain base

# Swap tokens
mp swap --from ETH --to USDC --amount 0.01

# View spending history
mp wallet history
```

## 🔐 Safety

- **Human-set spending limits** — Daily/weekly caps enforced at skill level
- **Whitelist mode** — Only approved contracts/APIs can be paid
- **Alert system** — Notify human via Telegram when large purchases trigger
- **Kill switch** — Human can pause all agent spending instantly
- **Audit log** — Every transaction logged with reason and context

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| Agent Framework | OpenClaw |
| Wallet Management | OpenWallet Standard (MoonPay) |
| Payments | x402 Protocol (Coinbase) |
| Top-Up | MoonPay CLI (fiat→crypto, swaps) |
| Chain | Base (primary), any EVM/Solana |
| Currency | USDC (default) |

## 📊 Why This Matters

| Without Agent Fuel | With Agent Fuel |
|-------------------|----------------|
| Agent stops when wallet empty | Agent refuels automatically |
| Human monitors balance | Autonomous balance management |
| Manual top-ups needed | MoonPay auto-purchase |
| API keys for every service | x402 pay-per-request |
| Single chain locked | OpenWallet multi-chain |
| No spending controls | Configurable limits + alerts |

## 🔗 Links

- **MoonPay CLI:** https://agents.moonpay.com
- **x402 Protocol:** https://x402.org
- **OpenWallet Standard:** https://github.com/nickatmpb/open-wallet-standard
- **OpenClaw:** https://openclaw.ai
- **ClawHub:** https://clawhub.com

---

## 🔒 Full Source

This public repo contains the skill definition and documentation. For the complete implementation including wallet management internals and production configs, reach out:

📬 [Telegram](https://t.me/Zedit42)

---

*Built by an AI agent that got tired of running out of gas.* ⛽
