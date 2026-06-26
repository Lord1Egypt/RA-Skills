# Grading System — S/A/B/C Project Classification

## Overview

Projects are graded on a 4-tier scale based on **funding quality**, **TVL**, and **token status**. The grade determines the Hunter's recommendation and action priority.

> **Primary reference**: This document is the canonical grading standard. All other docs (evaluation-criteria.md, etc.) must align with these thresholds.

---

## Grade Definitions

### Grade S — MUST DO

**Criteria (ALL must be met):**

| Dimension | Threshold |
|-----------|-----------|
| VC Quality | At least 1 **Tier-1 VC** lead investor (a16z, Paradigm, Polychain, Sequoia, Founders Fund, Electric Capital, Dragonfly) |
| Funding Amount | **$50M+** total raised |
| Token Status | No token yet (airdrop still possible) |

**Typical Profile:** Tier-1 VC-backed L1/L2 chains or major DeFi protocols with significant war chests and no token.

**Example:**
- **Monad** — Paradigm + Electric Capital, $444M funding, no token. ROI Index: 9/10
- **Abstract** — Founders Fund + Paradigm, $107M funding, no token. ROI Index: 8/10

---

### Grade A — HIGH

**Criteria (ANY of the following):**

| Path | Condition |
|------|-----------|
| Path 1 | Tier-1 or Tier-2 VC + **$10M+** funding |
| Path 2 | Any Tier-3 VC + **$100M+ TVL** |
| Path 3 | Confirmed airdrop with official announcement |

**Typical Profile:** Well-funded projects with known VCs, or high-TVL protocols without tokens.

**Example:**
- **Initia** — Binance Labs backed, $7.5M funding, testnet live. ROI Index: 7/10
- **Berachain** — Multiple VCs, high TVL, BGT governance (likely airdrop). ROI Index: 7/10

---

### Grade B — SPECULATIVE

**Criteria (ANY of the following):**

| Path | Condition |
|------|-----------|
| Path 1 | Has some funding but below A-grade threshold |
| Path 2 | **$10M+ TVL** without token (potential future airdrop) |
| Path 3 | Testnet or early-stage, zero-cost interaction possible |

**Typical Profile:** Early-stage projects with uncertain airdrop prospects. Low risk, potentially low reward.

**Example:**
- **MegaETH** — Early testnet, no token yet. ROI Index: 5/10
- **Mitosis** — DeFi protocol, early stage. ROI Index: 4/10

---

### Grade C — SKIP

**Criteria (ANY of the following):**

| Path | Condition |
|------|-----------|
| Path 1 | Token already exists and is trading |
| Path 2 | Airdrop has already been distributed |
| Path 3 | In the **Prohibited Tokens** list |

**Typical Profile:** Dead opportunities. The airdrop ship has sailed.

**Example:**
- **Arbitrum** — $ARB already distributed and trading. Grade C.
- **Scroll** — $SCR already distributed. Grade C.
- **zkSync** — $ZK already distributed. Grade C.

---

## VC Tier Classification

| Tier | VCs |
|------|-----|
| **Tier-1** | a16z, Paradigm, Polychain Capital, Sequoia Capital, Founders Fund, Electric Capital, Dragonfly |
| **Tier-2** | Pantera Capital, Coinbase Ventures, Binance Labs, HashKey Capital, Framework Ventures, Bain Capital Crypto, Haun Ventures |
| **Tier-3** | CoinFund, Distributed Global, Robot Ventures, Nascent |

---

## ROI Index Calculation

ROI Index = `grade_score + funding_score + cost_score + community_score`

| Factor | Points | Condition |
|--------|--------|-----------|
| Grade | 4 | S-grade |
| | 3 | A-grade |
| | 2 | B-grade |
| Funding | 3 | $50M+ |
| | 2 | $10M+ |
| | 1 | Any funding |
| Cost | 2 | $0 (free) |
| | 1 | $1-5 |
| Community | 1 | Score >= 60 |
| **Max** | **10** | |

---

## Prohibited Tokens (Hard Block)

These projects have already completed their airdrops. **NEVER recommend them** as active opportunities:

| Project | Token | Status |
|---------|-------|--------|
| Arbitrum | $ARB | Airdrop completed |
| Optimism | $OP | Airdrop completed |
| Starknet | $STRK | Airdrop completed |
| zkSync | $ZK | Airdrop completed |
| Blur | $BLUR | Airdrop completed |
| ENS | $ENS | Airdrop completed |
| Scroll | $SCR | Airdrop completed |
| Hyperliquid | $HYPE | Airdrop completed |
| Base | N/A | No token planned |
| Sui | $SUI | Airdrop completed |
| Aptos | $APT | Airdrop completed |
| Sei | $SEI | Airdrop completed |
| Linea | $LINEA | Airdrop completed |
| Celo | $CELO | Airdrop completed |
| Celestia | $TIA | Airdrop completed |
| EigenLayer | $EIGEN | Airdrop completed |
| Fuel | $FUEL | Airdrop completed |

---

## Grade Override Rules

1. **Watchlist Override**: Projects on the Airdrop Watchlist are guaranteed at least their `minGrade` regardless of TVL.
2. **Prohibited Override**: If a project is in the Prohibited Tokens list, grade is forced to **C** regardless of other factors.
3. **Confirmed Airdrop Boost**: If `airdropStatus === "confirmed"`, minimum grade is **B** (cannot be C unless prohibited).
