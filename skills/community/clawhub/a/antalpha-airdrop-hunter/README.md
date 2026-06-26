# Airdrop Hunter

**Elite Web3 Airdrop Strategist — From Clueless to Deadly**

[![Skill Version](https://img.shields.io/badge/version-1.3.0-blue.svg)](https://github.com/AntalphaAI/airdrop-hunter)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

---

## Overview

Airdrop Hunter doesn't just find airdrops. It turns you into a hunter.

We cut through the noise of 90% trash airdrop info and deliver a **guided workflow**: Discover -> Verify -> Strategize. Every response includes a **Next Step** so you're never left wondering "now what?"

**What You Get:**
- S/A/B graded opportunities — stop digging for trash
- Scam shield — verify before you connect your wallet
- Zero-cost starter pack — no ETH? No problem
- Guided hunting — every tool tells you what to do next

---

## Features

### 1. Data-Driven Scanning (MCP Version)
The MCP Server version fetches structured data directly from:
- **DefiLlama API** - Protocol TVL, categories, chain info
- **Hard-coded Funding Database** - VC backing, funding amounts
- **Airdrop Watchlist** - Curated S/A-grade projects

### 2. Project Grading System

| Grade | Criteria | Action |
|-------|----------|--------|
| **S** | Tier-1 VC backing (a16z, Paradigm), $50M+ funding | MUST DO |
| **A** | Reputable VCs, $10M+ funding, confirmed token | HIGH |
| **B** | Testnet stage, zero-cost, early potential | SPECULATIVE |

### 3. Minimalist Output
No fluff. Direct delivery of:
```
[Project] + [Action] + [Cost/Faucet Link]
```

### 4. Security Scanning
- Domain verification against known official domains
- Phishing pattern detection (hyphenated knockoffs, subdomain phishing)
- Fake claim website detection

---

## MCP Server Version (Recommended)

The latest version of Airdrop Hunter runs as an MCP tool on the Antalpha MCP Server.

**Repository**: [antalpha-com/antalpha-skills](https://github.com/antalpha-com/antalpha-skills) (`feat/airdrop-hunter` branch)

**No plugins or API keys required.** All data is fetched from public APIs (DefiLlama).

### Your Arsenal — 5 Tools in 3 Tactical Categories

| Category | Tool | Alias | What It Does | When to Use |
|----------|------|-------|-------------|-------------|
| **Intelligence** | `airdrop-scan` | The Radar | Sweep the market for S/A/B graded airdrops with TVL, funding, VC data | Want to see what's hot right now |
| **Intelligence** | `airdrop-daily-report` | The Daily Brief | 4-section morning report: top priority, zero-cost, deadlines, scam alerts | Planning your day, catching up after time away |
| **Due Diligence** | `airdrop-check-project` | The Sniff Test | Grade any project on the spot (S/A/B/C), detect completed airdrops | Someone mentioned a project, want to know if it's worth your time |
| **Due Diligence** | `airdrop-scam-check` | The Shield | Verify URLs/projects for phishing, fake claims, suspicious domains | Found an airdrop link on Twitter/Telegram, something feels off |
| **Starter Pack** | `airdrop-zero-cost` | The Broke-to-Rich Path | Find $0 cost testnet & free mainnet opportunities | New to hunting, on a budget, want risk-free starts |

### Workflow — Discover, Verify, Strategize

```
Step 1: DISCOVER          Step 2: VERIFY             Step 3: STRATEGIZE
┌──────────────┐     ┌───────────────────┐     ┌───────────────────┐
│ airdrop-scan │────>│ airdrop-check-    │────>│ airdrop-zero-cost │
│   The Radar  │     │   project         │     │ Broke-to-Rich     │
│              │     │   The Sniff Test  │     │                   │
│ airdrop-     │     │                   │     │ Find free ways to │
│ daily-report │     │ airdrop-scam-     │     │ qualify for the   │
│ The Daily    │     │   check           │     │ airdrops you just │
│   Brief      │     │   The Shield      │     │ verified          │
└──────────────┘     └───────────────────┘     └───────────────────┘
```

**Every tool response includes a `next_step` recommendation** that tells you exactly which tool to call next and why — so you're never left wondering "what do I do now?"

### Next Step Examples

| You just... | Hunter's Recommendation |
|-------------|------------------------|
| Scanned and found an S-grade project | "Run `airdrop-check-project` to deep-dive before you interact" |
| Checked a project that's Grade C (completed) | "Stop wasting time. Run `airdrop-scan` to find fresh opportunities" |
| Found a promising A-grade project with a website | "Run `airdrop-scam-check` on that URL before you connect your wallet" |
| Checked a scam URL (critical risk) | "Stay AWAY. Run `airdrop-check-project` to find the real official site" |
| Got zero-cost opportunities | "Run `airdrop-scam-check` on the official URL to verify it's safe" |
| Daily report shows scam alerts | "Run `airdrop-scam-check` on any suspicious links you've seen" |

---

### Installation

1. Download `airdrop-hunter.skill`
2. Upload to Skill library
3. Test with command: `daily report`

### Quick Commands

| Command | Action |
|---------|--------|
| `daily report` | Get latest 24-hour airdrop checklist |
| `any zero-cost?` | Filter for free testnet opportunities |
| `check [project]` | Get specific project airdrop status |
| `S-grade tasks` | Show only Grade S high-priority tasks |

---

## Sample Output

```
Airdrop Scan Results (2026-04-13)

TOP PRIORITY (Grade S)
1. Monad: Testnet interaction | $0 | No deadline
   Why: Paradigm + Electric Capital ($444M funding), Tier-1 VC
   Link: https://monad.xyz

2. Abstract: Bridge + Swap tasks | $1-5 | Ongoing
   Why: Founders Fund + Paradigm ($107M funding)
   Link: https://abstract.xyz

ZERO-COST (Grade B)
1. Initia: Testnet participation | Free | Ongoing
   Why: Binance Labs backed, testnet live
   Link: https://initia.xyz

SCAM ALERTS
- Phishing: "scroll-airdrop-claim.xyz" is NOT official
- Official: scroll.io
```

---

## Case Review

### Case 1: Daily Airdrop Scan

**User**: "What airdrop opportunities are available right now?"

**Tool**: `airdrop-scan`

**Rendered output**:
```
Airdrop Scan (2026-04-13) — 18 opportunities found

[S] Monad | Chain | $0 | monad.xyz
    Paradigm + Electric Capital ($444M) | No token yet

[S] Abstract | Chain | $1-5 | abstract.xyz
    Founders Fund + Paradigm ($107M) | TVL $52M

[A] Initia | DEX | $0 | initia.xyz
    Binance Labs ($7.5M) | Testnet live

... and 15 more
```

---

### Case 2: Daily Report

**User**: "Give me today's airdrop report"

**Tool**: `airdrop-daily-report`

**Rendered output**:
```
Airdrop Daily Report — 2026-04-13

TOP PRIORITY (S/A Grade)
 1. Monad [S] | Testnet | $0 | Paradigm + Electric Capital ($444M)
 2. Abstract [S] | Bridge+Swap | $1-5 | Founders Fund + Paradigm ($107M)

ZERO-COST OPPORTUNITIES
 1. Initia — Testnet participation (free)
 2. MegaETH — Testnet interaction (free)

UPCOMING DEADLINES
 1. Berachain [A] — BGT staking active, token likely

SCAM ALERTS
 ! Hyphenated knockoff domains (e.g., project-airdrop.io) — ALWAYS verify
 ! Official projects NEVER DM claim links
```

---

### Case 3: Check Specific Project

**User**: "Is Scroll still worth doing?"

**Tool**: `airdrop-check-project` with `project_name: "Scroll"`

**Rendered output**:
```
Scroll — Grade C | Airdrop COMPLETED

Token: $SCR (already trading)
TVL: $620M | Funding: $80M (Polychain, Sequoia)

Status: Airdrop already distributed. SCR is live.
Warning: Beware of fake "Scroll airdrop" websites — official is scroll.io

Recommendation: SKIP — no further airdrop opportunity
```

---

### Case 4: Zero-Cost Opportunities

**User**: "Any free airdrops I can do without spending gas?"

**Tool**: `airdrop-zero-cost`

**Rendered output**:
```
Zero-Cost Airdrops — 3 found

1. Monad (Testnet) | monad.xyz
   Interact with testnet dApps — no real ETH needed

2. Initia (Testnet) | initia.xyz
   Testnet swaps + LP — free test tokens from faucet

3. MegaETH (Testnet) | megaeth.com
   Early testnet participation — free to join
```

---

### Case 5: Scam Check

**User**: "Is scroll-airdrop-claim.xyz legit?"

**Tool**: `airdrop-scam-check` with `url: "https://scroll-airdrop-claim.xyz"`

**Rendered output**:
```
SCAM ALERT — Risk Level: CRITICAL

URL: scroll-airdrop-claim.xyz

Warnings:
 [CRITICAL] Hyphenated knockoff domain — "scroll-airdrop" pattern detected
 [CRITICAL] Uses "scroll" name but is NOT the official project

Safe alternative: scroll.io

DO NOT connect your wallet. This is a phishing site.
```

---

### Case 6: Scam Check (Safe URL)

**User**: "Is berachain.com the real site?"

**Tool**: `airdrop-scam-check` with `url: "https://berachain.com"`, `project_name: "Berachain"`

**Rendered output**:
```
SAFE — berachain.com is the verified official domain for Berachain.

No warnings detected. You can proceed with caution.
Always verify URLs independently before connecting your wallet.
```

---

## Project Structure

### MCP Server Version
```
libs/skills/airdrop-hunter/
├── src/
│   ├── airdrop-hunter.config.ts     # Configuration
│   ├── airdrop-hunter.module.ts     # NestJS module
│   ├── constants/
│   │   ├── prohibited-tokens.ts     # Completed airdrops (exact match)
│   │   ├── funding-database.ts      # Hard-coded VC/funding data
│   │   ├── airdrop-watchlist.ts     # Curated S/A-grade projects
│   │   ├── vc-tiers.ts             # VC tier classification
│   │   └── scam-patterns.ts        # Phishing detection patterns
│   ├── model/
│   │   └── airdrop-project.model.ts # Data interfaces
│   ├── service/
│   │   ├── defillama.service.ts     # DefiLlama API client
│   │   ├── grading.service.ts       # S/A/B/C grading engine
│   │   ├── scam-detector.service.ts # Scam detection
│   │   └── airdrop-scanner.service.ts # Scan orchestrator
│   └── tools/
│       └── airdrop-hunter.tools.ts  # 5 MCP tool registrations
└── test/
    └── airdrop-hunter.test.ts       # 35 unit tests
```
---

## Disclaimer

**This tool is for informational purposes only. Not financial advice.**

- Always DYOR (Do Your Own Research)
- Never invest more than you can afford to lose
- Verify all information before interacting
- Use separate wallets for airdrop hunting
- Never share private keys or seed phrases

---

## License

MIT License
Maintainer: AntalphaAI Team
