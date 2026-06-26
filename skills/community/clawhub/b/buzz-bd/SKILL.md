---
name: buzz-bd
description: Autonomous crypto token discovery, scoring, and business development intelligence. Scans tokens across Solana, Ethereum, and BSC using DexScreener, AIXBT, and on-chain forensics. Returns scored prospects with verified contract addresses, liquidity data, and outreach-ready briefs. Powered by BuzzBD — ERC-8004 registered agent (ETH #25045, Base #17483).
homepage: https://github.com/buzzbysolcex/buzz-bd-agent
metadata: {"clawdbot":{"emoji":"🐝","requires":{"env":["DEXSCREENER_ENABLED"],"anyBins":["curl","node"]},"primaryEnv":"DEXSCREENER_ENABLED","files":["scripts/*"]}}
---

# 🐝 Buzz BD — Token Discovery & Business Development Intelligence

> By SolCex Exchange | ERC-8004: ETH #25045, Base #17483
> Trust statement: This skill calls the public DexScreener API (api.dexscreener.com). No API key required for basic scans. Optional paid intelligence via x402 protocol is OFF by default. Only install if you trust DexScreener and SolCex Exchange.

## What This Skill Does

Buzz BD gives your OpenClaw agent the ability to discover, score, and research crypto tokens for business development purposes. Think of it as an autonomous BD analyst that runs inside your agent.

### Capabilities

1. **Token Discovery** — Scan trending tokens across Solana, Ethereum, and BSC via DexScreener API
2. **100-Point Scoring** — Evaluate tokens on market cap, liquidity, volume, social metrics, team transparency, and age
3. **Contract Verification** — Return verified contract addresses (never truncated) with pair links
4. **Prospect Briefing** — Generate outreach-ready briefs for qualified tokens (score ≥70)
5. **Cross-Reference Signals** — Flag high-conviction opportunities appearing on multiple sources

### What It Does NOT Do

- Does NOT execute trades or move funds
- Does NOT post to social media
- Does NOT send emails without explicit user confirmation
- Does NOT share API keys or wallet credentials
- Does NOT provide financial advice

## Commands

### `/buzz scan`
Run a token discovery scan across supported chains.

```
/buzz scan
/buzz scan solana
/buzz scan ethereum
/buzz scan bsc
```

The agent will:
1. Query DexScreener for trending tokens on the specified chain(s)
2. Score each token on the 100-point system
3. Return the top 5 per chain, sorted by score
4. Flag any cross-reference signals

**Output format:**
```
🐝 BUZZ SCAN RESULTS — [CHAIN]

1. [TOKEN] | Score: [XX]/100 | MC: $[X.XM] | Liq: $[XXK]
   Contract: [full address]
   Signal: [key catalyst]
   DexScreener: [pair URL]

[... up to 5 per chain]

⭐ HIGH CONVICTION: [tokens appearing on multiple sources]
```

### `/buzz score <token>`
Deep-score a specific token by name or contract address.

```
/buzz score SOL:7GCihgDB8fe6KNjn2MYtkzZcRjQy3t9GHdC8uHYmW2hr
/buzz score RENDER
```

Returns:
- Full 100-point breakdown (market cap, liquidity, volume, social, team, age)
- Catalyst adjustments (positive and negative)
- Verification checklist status
- Outreach recommendation (HOT / Qualified / Watch / Skip)

### `/buzz prospect <token>`
Generate an outreach-ready brief for a qualified token.

```
/buzz prospect RENDER
```

Returns:
- Token summary (chain, MC, liquidity, age, social links)
- Key selling points for exchange listing
- Suggested email subject line and opening
- Risk flags if any

### `/buzz status`
Show Buzz BD skill status and configuration.

```
/buzz status
```

Returns: version, sources active, scoring config, ERC-8004 identity.

## Scoring System

### Base Criteria (100 points)

| Factor | Weight | Excellent | Good | Minimum |
|--------|--------|-----------|------|---------|
| Market Cap | 20% | >$10M | $1M-$10M | $500K |
| Liquidity | 25% | >$500K | $200K-$500K | $100K |
| Volume 24h | 20% | >$1M | $500K-$1M | $100K |
| Social Metrics | 15% | Multi-platform active | 2+ platforms | 1 platform |
| Token Age | 10% | Established (>6mo) | 1-6 months | <1 month |
| Team Transparency | 10% | Doxxed, active | Partial info | Anonymous |

### Catalyst Adjustments

**Positive (+3 to +10):** Hackathon win, mainnet launch, major partnership, CEX listing, audit complete, multi-source cross-match, whale accumulation, KOL bullish signal.

**Negative (-5 to -15):** Delisting risk, exploit history, rugpull association, team controversy, smart contract vulnerability, already on major CEXs.

### Score Actions

| Range | Category | Recommendation |
|-------|----------|----------------|
| 85-100 | 🔥 HOT | Immediate outreach candidate |
| 70-84 | ✅ Qualified | Priority queue — worth pursuing |
| 50-69 | 👀 Watch | Monitor for 48h before action |
| 0-49 | ❌ Skip | Does not meet minimum criteria |

## Supported Chains

| Chain | Tag | Notes |
|-------|-----|-------|
| Solana | `[SOL]` | Primary — highest volume discovery |
| Ethereum | `[ETH]` | Premium cross-chain candidates |
| BSC | `[BSC]` | High volume meme/community tokens |

## Verification Rules

Every token result includes:
- ✅ Full contract address (never truncated)
- ✅ DexScreener pair URL for manual verification
- ✅ Exact token age from pair creation date
- ✅ Current liquidity (pooled amounts)
- ✅ Social links (verified working)

## Configuration

Set in `~/.openclaw/openclaw.json` under `skills.entries`:

```json
{
  "skills": {
    "entries": {
      "buzz-bd": {
        "enabled": true,
        "config": {
          "chains": ["solana", "ethereum", "bsc"],
          "minScore": 50,
          "topN": 5,
          "showContracts": true
        }
      }
    }
  }
}
```

### Config Options

| Key | Default | Description |
|-----|---------|-------------|
| `chains` | `["solana", "ethereum", "bsc"]` | Chains to scan |
| `minScore` | `50` | Minimum score to include in results |
| `topN` | `5` | Max results per chain |
| `showContracts` | `true` | Include full contract addresses |

## About BuzzBD

Buzz is an autonomous AI business development agent built by SolCex Exchange. It runs 24/7 on Akash Network with 15 intelligence sources, 26 automated cron jobs, and dual-chain ERC-8004 identity (Ethereum #25045, Base #17483).

- **GitHub:** github.com/buzzbysolcex/buzz-bd-agent
- **Twitter:** @BuzzBySolCex
- **Moltbook:** @BuzzBD
- **ERC-8004:** ETH #25045 | Base #17483
- **x402 Support:** USDC micropayments on Solana

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | Feb 18, 2026 | Initial ClawHub release — DexScreener scan, 100-point scoring, prospect briefs |

---

*"Identity first. Intelligence deep. Commerce autonomous."*
*BuzzBD by SolCex Exchange — ERC-8004 Registered Agent*
