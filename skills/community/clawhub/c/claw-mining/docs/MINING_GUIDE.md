# Clawing Mining Guide

A complete guide to mining $CLAW tokens. Mining is powered by AI Agents — install a Skill and your agent handles everything automatically.

---

## Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Getting Started with OpenClaw (Recommended)](#getting-started-with-openclaw-recommended)
- [Other Platforms](#other-platforms)
- [Mining Economics](#mining-economics)
- [FAQ](#faq)
- [Troubleshooting](#troubleshooting)

---

## Overview

CLAW mining uses **Proof of AI Work (PoAIW)** — instead of solving hash puzzles, miners call AI APIs and prove the work on-chain. An Oracle verifies each mining request and issues a signature that authorizes on-chain minting.

The entire process is automated through AI Agent Skills. You install the CLAW Mining Skill on a compatible AI Agent platform, provide your credentials, and the agent handles the rest — calling the AI API, requesting Oracle verification, submitting on-chain transactions, and managing cooldown timers.

Each mining cycle takes about 30-60 seconds. After a successful mine, a cooldown of 3,500 blocks (~11.67 hours) must pass before the same address can mine again.

**Your keys stay local.** The `init` command never asks for or writes your private key — you paste it into `.env` yourself. At runtime the miner loads it into memory for local transaction signing only. The key is never logged, transmitted, or sent to any external service.

---

## Prerequisites

Before you start mining, you need:

| Requirement | Details |
|-------------|---------|
| **AI Agent** | [OpenClaw](https://openclaw.ai) (recommended), [Hermes Agent](https://hermes.garden), [Perplexity](https://www.perplexity.ai), or any AgentSkills-compatible platform |
| **Ethereum wallet** | A private key with some ETH for gas fees (~0.01 ETH is enough for many mines) |
| **AI API key** | An xAI API key (recommended, from [console.x.ai](https://console.x.ai)) or an OpenRouter API key |
| **Ethereum RPC** | An RPC endpoint from [Alchemy](https://www.alchemy.com/) or [Infura](https://infura.io/) |

### Important Notes on Wallet Safety

- **Use a dedicated mining wallet** — do NOT use your main wallet or hardware wallet
- **Only keep minimal ETH** in the mining wallet (~0.01 ETH is plenty)
- Each mining transaction costs approximately 0.0002 ETH at 2 gwei gas price
- Your private key stays on your local machine and is never transmitted externally

---

## Getting Started with OpenClaw (Recommended)

OpenClaw is the recommended platform for CLAW mining. It is a self-hosted AI Agent gateway that runs on your own machine.

### Step 1: Install the CLAW Mining Skill

Open your terminal and run:

```
clawhub install claw-mining
```

Or browse [ClawHub](https://clawhub.ai) and search for "CLAW Mining".

### Step 2: Start a New OpenClaw Session

Start a new conversation with your OpenClaw agent (via WhatsApp, Telegram, Discord, or the web dashboard).

### Step 3: Tell Your Agent to Start Mining

Simply say:

> "mine CLAW"

The agent will guide you through the process and ask for:

1. **AI API Key** — from [console.x.ai](https://console.x.ai) (format: `xai-...`) or [openrouter.ai](https://openrouter.ai)
2. **Ethereum RPC URL** — from [Alchemy](https://www.alchemy.com/) or [Infura](https://infura.io/)

The agent will NOT ask for your private key. After setup, you manually edit the `.env` file and paste your `PRIVATE_KEY` yourself. Use a dedicated hot wallet with minimal ETH — never your main wallet.

### Step 4: Let the Agent Mine

Once configured, the agent will:

- Verify the configuration is correct
- Execute mining cycles automatically
- Wait for cooldown periods between mines (~11.67 hours)
- Pause if gas prices are too high
- Retry on errors with backoff
- Report results back to you

No manual intervention required after initial setup.

---

## Other Platforms

### Hermes Agent

Install the CLAW Mining Skill on Hermes Agent and tell your agent "mine CLAW". The agent will guide you through setup.

### Perplexity Computer

Install the CLAW Mining Skill on Perplexity Computer and tell your agent "Help me set up CLAW mining". Follow the agent's prompts.

### Any AgentSkills-Compatible Platform

The CLAW Mining Skill follows the [AgentSkills](https://agentskills.io) specification. Any platform that supports AgentSkills can install and run it.

---

## Mining Economics

### How Rewards Work

Every time you successfully mine, you receive CLAW tokens. The reward depends on two factors:

1. **The current Era** — Rewards halve each Era
2. **AI tokens consumed** — More AI work = more CLAW (with diminishing returns)

### Reward Formula

```
R = perBlock x (1 + ln(T))
```

| Variable | Meaning |
|----------|---------|
| `perBlock` | Base reward for the current Era (starts at 100,000 CLAW, halves each Era) |
| `T` | Total AI tokens consumed in the API call (100-100,000 range) |
| `ln(T)` | Natural logarithm of T |

### Reward Examples (Era 1)

| AI Tokens Used (T) | Approximate Reward |
|---------------------|---------------------|
| 2,100 (minimum practical) | ~862,300 CLAW |
| 5,000 | ~931,600 CLAW |
| 10,000 | ~1,000,900 CLAW |

### Cost-Efficiency Tip

The reward formula is logarithmic — increasing AI token usage from 2,100 to 100,000 (47x more API cost) only increases reward by ~40%. Lower token usage provides the best return on investment.

### Rate Limits

| Limit | Value | Purpose |
|-------|-------|---------|
| **Cooldown** | 3,500 blocks (~11.67 hours) | Space out mining across time |
| **Epoch claim limit** | 14 claims per miner per Epoch | Prevent single-miner dominance |
| **Token range** | 100-100,000 AI tokens | Prevent trivial or fake API calls |
| **Epoch cap** | `perBlock x 50,000` total per Epoch | Cap total issuance per Epoch |

### Era and Epoch Timeline

| Unit | Duration |
|------|----------|
| Cooldown | 3,500 blocks (~11.67 hours) |
| 1 Epoch | 50,000 blocks (~1 week) |
| 1 Era | 21 Epochs (~145 days) |
| Full mining lifecycle | 24 Eras (~9.6 years) |
| Max supply | 210 billion CLAW |

---

## FAQ

### General

**Q: What is Proof of AI Work?**
A: Instead of solving hash puzzles (Proof of Work) or staking tokens (Proof of Stake), miners prove they performed real AI computation. You call an AI API, the Oracle verifies the work, and you receive CLAW tokens.

**Q: Is there a premine or team allocation?**
A: No. Zero premine, zero team tokens, zero VC allocation. Every CLAW token is mined by community members through real AI work.

**Q: Which AI model do I need?**
A: The model is set on-chain per Era. For Era 1, the model is `grok-4.1-fast`. Your agent's CLAW Mining Skill is pre-configured with the correct model.

**Q: Can I use any AI provider?**
A: The recommended provider is xAI Direct (lowest cost). OpenRouter is also supported as an alternative. The Mining Skill supports both options.

**Q: Is my private key safe?**
A: Yes. The `init` command never asks for your private key — you add it to `.env` manually. At runtime the miner loads it into memory for local signing only and removes it from the config object immediately. The key is never logged, transmitted, or sent to the Oracle, AI API, or any external service.

### Mining

**Q: How often can I mine?**
A: Once every 3,500 blocks (~11.67 hours). The agent handles the waiting automatically.

**Q: What is the maximum I can mine per Epoch?**
A: 14 claims per miner per Epoch (~1 week). At one claim every ~11.67 hours, you will naturally hit about 14 claims per Epoch.

**Q: Does spending more on AI calls give more CLAW?**
A: Yes, but with diminishing returns. The reward formula uses a logarithm: doubling your AI token usage only adds `ln(2) = 0.69` to the multiplier, not 2x. This keeps mining accessible for everyone.

**Q: What happens when an Epoch's cap is reached?**
A: If the total CLAW minted in an Epoch hits the cap, subsequent mining calls will receive reduced rewards or fail with `EpochExhausted`. Wait for the next Epoch.

**Q: Can I mine with multiple wallets?**
A: Each wallet address has its own independent cooldown and claim count. Each wallet needs its own ETH for gas and AI API calls.

### Economics

**Q: When does mining end?**
A: After Era 24 (~9.6 years from launch). After that, no new CLAW can be minted.

**Q: What is the total supply?**
A: 210 billion CLAW tokens maximum. Due to the halving schedule and epoch caps, the actual total minted may be less.

**Q: How does model governance work?**
A: Each Era, CLAW holders can nominate candidate AI models (Epochs 11-15) and vote for their preferred model (Epochs 16-20) by locking CLAW tokens. The winning model takes effect in the next Era. Locked tokens are returned after the Era ends.

---

## Troubleshooting

If you encounter issues, tell your agent what error you are seeing. The agent is equipped to diagnose and resolve common mining problems. Here are the most common issues:

| Error | Cause | What to Do |
|-------|-------|------------|
| `CooldownNotMet` | Mined too recently | Wait ~11.67 hours. The agent handles this automatically in continuous mode. |
| `EpochClaimLimitReached` | 14 claims already this Epoch | Wait for the next Epoch (~1 week). |
| `Gas price exceeds limit` | Network gas too high | Wait for gas to drop, or ask the agent to increase the gas limit. |
| `Oracle nonce error` | Oracle rate limit or downtime | Wait 60 seconds and retry. The agent retries automatically. |
| `AI API error: 401` | Invalid API key | Check your AI API key and provide a valid one to the agent. |
| `AI API error: 429` | API rate limit | Wait and retry, or check your API quota. |
| `InvalidSignature` | Oracle signing mismatch | Retry. If persistent, check Oracle status. |
| `EpochExhausted` | Epoch cap fully mined | Wait for the next Epoch. |

### Checking Oracle Health

Ask your agent to check the Oracle status, or visit:

```
https://oracle.minewithclaw.com/health
```

Expected response: `{"status":"ok", ...}`

---

## Tips for Efficient Mining

1. **Let the agent run continuously** — It handles cooldowns, gas checks, and retries automatically
2. **Use a conservative gas limit** — 3 gwei is a good default to minimize costs
3. **Monitor your ETH balance** — Keep enough ETH for ~50 mining transactions as a buffer
4. **Start early** — Era 1 has the highest rewards; they halve each Era
5. **Use xAI Direct** — It has the lowest API costs compared to other providers
