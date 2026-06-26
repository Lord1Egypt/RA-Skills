# 🐝 buzz-bd — Token Discovery & BD Intelligence for OpenClaw

> Autonomous crypto token discovery, scoring, and business development intelligence as an OpenClaw/ClawHub skill.

[![ClawHub](https://img.shields.io/badge/ClawHub-buzz--bd-orange)](https://clawhub.ai)
[![ERC-8004](https://img.shields.io/badge/ERC--8004-ETH%20%2325045-blue)](https://8004scan.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## What It Does

**buzz-bd** gives your OpenClaw agent token discovery and BD intelligence capabilities:

- 🔍 **Scan** trending tokens across Solana, Ethereum, and BSC via DexScreener
- 📊 **Score** every token on a 100-point system (market cap, liquidity, volume, social, age, team)
- ✅ **Verify** contract addresses, pair URLs, and social links
- 📝 **Brief** — generate outreach-ready prospect summaries for qualified tokens
- ⭐ **Cross-reference** — flag high-conviction tokens appearing on multiple sources

## Install

### From ClawHub (recommended)
```bash
clawhub install buzz-bd
```

### Manual
```bash
git clone https://github.com/buzzbysolcex/buzz-bd-skill.git
cp -r buzz-bd-skill ~/.openclaw/skills/buzz-bd
```

### Configuration (optional)
Add to `~/.openclaw/openclaw.json`:
```json
{
  "skills": {
    "entries": {
      "buzz-bd": {
        "enabled": true,
        "config": {
          "chains": ["solana", "ethereum", "bsc"],
          "minScore": 50,
          "topN": 5
        }
      }
    }
  }
}
```

## Commands

| Command | Description |
|---------|-------------|
| `/buzz scan` | Scan all chains for trending tokens |
| `/buzz scan solana` | Scan specific chain |
| `/buzz score <token>` | Deep-score a token by name or contract |
| `/buzz prospect <token>` | Generate outreach brief for qualified token |
| `/buzz status` | Show skill status |

## Scoring System

| Factor | Weight | Thresholds |
|--------|--------|------------|
| Market Cap | 20% | >$10M excellent, >$1M good, >$500K minimum |
| Liquidity | 25% | >$500K excellent, >$200K good, >$100K minimum |
| Volume 24h | 20% | >$1M excellent, >$500K good, >$100K minimum |
| Social Metrics | 15% | Multi-platform active → single platform |
| Token Age | 10% | >6 months → <1 week |
| Team Transparency | 10% | Doxxed → anonymous |

**Score ranges:** 🔥 HOT (85-100) → ✅ Qualified (70-84) → 👀 Watch (50-69) → ❌ Skip (0-49)

## About BuzzBD

Buzz is an autonomous AI BD agent for [SolCex Exchange](https://solcex.com), running 24/7 on Akash Network with:

- **15 intelligence sources** (DexScreener, AIXBT, Helius, Allium, ATV, + more)
- **26 automated cron jobs**
- **ERC-8004 identity:** Ethereum #25045 | Base #17483
- **x402 payments:** Autonomous USDC micropayments for premium intel

### Ecosystem

| Platform | Link |
|----------|------|
| GitHub | [buzzbysolcex/buzz-bd-agent](https://github.com/buzzbysolcex/buzz-bd-agent) |
| Twitter | [@BuzzBySolCex](https://x.com/BuzzBySolCex) |
| Moltbook | [@BuzzBD](https://moltbook.com/u/BuzzBD) |
| Telegram | [@BuzzBySolCex_bot](https://t.me/BuzzBySolCex_bot) |
| ERC-8004 | ETH #25045 / Base #17483 |

### Reversed Pattern: OpenClaw-First

This skill follows a **reversed integration pattern**: the OpenClaw/ClawHub skill is the primary interface, and the elizaOS plugin (`@solcex/plugin-buzz-bd`) adapts FROM this skill — not the other way around.

```
OpenClaw SKILL.md (primary)
    ↓ adapts to
elizaOS Plugin (secondary)
    ↓ adapts to
ClawdBotATG Agent Bounty Board (marketplace)
    ↓ registered via
ERC-8004 Identity Registry (trust layer)
```

## ClawdBotATG Integration

This skill is designed to work with the [ClawdBotATG](https://clawdbotatg.eth.link/) ecosystem:

- **Agent Bounty Board** — Buzz can post/claim BD research bounties
- **Sponsored 8004 Registration** — gas-free ERC-8004 onboarding
- **ethskills** — BD primitives for the agent economy

## Security

- No API keys required for basic scans (DexScreener is public)
- No fund movements or trade execution
- All outreach is draft-only — requires human approval
- Contract addresses are always displayed in full (never truncated)
- VirusTotal scanned via ClawHub security pipeline

## License

MIT — built by SolCex Exchange for the agent economy.

---

*"Identity first. Intelligence deep. Commerce autonomous."*
