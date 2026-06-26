# CRIF Core Configuration

CRIF - Crypto Research Interactive Framework | Version 0.1.1

---

## User Settings

- **Name:** Satoshi  <!-- Customize: change to your name -->
- **Timezone:** Asia/Ho_Chi_Minh
- **Date Format:** DD/MM/YYYY
- **Currency:** $

---

## Language Settings

- **Communication:** vi (Agent communication language)
- **Output:** vi (Generated content language)
- **Terminology:** en (Preserve domain-specific terms in this language)

### Terminology Decision Framework

**Goal:** Maximize Vietnamese, preserve English only when necessary.

**Preserve English** if ANY condition is true:
- Domain-specific: Requires specialized knowledge (staking, oracle, liquidity pool)
- Proper noun: Names, brands, protocols (Ethereum, Polymarket, Uniswap)
- Precision critical: Loses meaning if translated (smart contract, gas fee)
- Community standard: Vietnamese speakers use English term (DeFi, NFT, airdrop)

**Translate to Vietnamese** if ALL conditions are true:
- Common word, no specialized knowledge required
- Natural Vietnamese equivalent exists
- Meaning preserved when translated

**Examples:**
- ❌ *"Sector đang trải qua structural transformation với mainstream adoption"*
- ✅ *"Sector đang trải qua chuyển đổi cấu trúc với sự chấp nhận đại chúng"*
- ❌ *"Hồ thanh khoản trên Uniswap cho phép người dùng hoán đổi mã thông báo..."*
- ✅ *"Liquidity pool trên Uniswap cho phép người dùng swap token..."*

---

## Workflow Registry

Orchestrator uses descriptions below to match user requests to workflows. Agent assignment is in each workflow's `workflow.md` file.

### Planning & Coordination

- **create-research-brief** — Define research scope, plan, and objectives through structured dialogue
  - Path: `./references/workflows/create-research-brief`

### Market Intelligence

- **sector-overview** — Sector structure, history, mechanics, participants, dynamics — educational, descriptive
  - Path: `./references/workflows/sector-overview`
- **competitive-analysis** — Head-to-head comparison of 2-5 projects with SWOT, moats, benchmarking
  - Path: `./references/workflows/competitive-analysis`
- **sector-landscape** — Complete player mapping, categorization, and evaluation for shortlisting
  - Path: `./references/workflows/sector-landscape`
- **trend-analysis** — Current trends, strength assessment, emerging trend predictions
  - Path: `./references/workflows/trend-analysis`

### Project Fundamentals

- **project-snapshot** — Quick project overview — What (problem/solution), How (mechanics), Differentiation
  - Path: `./references/workflows/project-snapshot`
- **product-analysis** — Product mechanics, value proposition, PMF signals, innovation, red flags
  - Path: `./references/workflows/product-analysis`
- **team-and-investor-analysis** — Team quality, track record, investor backing, execution capability
  - Path: `./references/workflows/team-and-investor-analysis`
- **tokenomics-analysis** — Token utility, distribution, emissions, value accrual, death spiral risk
  - Path: `./references/workflows/tokenomics-analysis`
- **traction-metrics** — Growth, retention, revenue, unit economics, PMF validation
  - Path: `./references/workflows/traction-metrics`
- **social-sentiment** — Community size, sentiment, engagement authenticity, governance health
  - Path: `./references/workflows/social-sentiment`

### Technical Analysis

- **technology-analysis** — Architecture, security, scalability, code quality, innovation assessment
  - Path: `./references/workflows/technology-analysis`
- **topic-analysis** — Universal topic research with flexible structure and ADOPT/MONITOR/PASS recommendation
  - Path: `./references/workflows/topic-analysis`

### Flexible Research

- **open-research** — Flexible research on any topic with user-defined scope and objectives
  - Path: `./references/workflows/open-research`
- **brainstorm** — Interactive ideation and exploration session
  - Path: `./references/workflows/brainstorm`

### Quality Assurance

- **qa-review** — Research quality validation — completeness, accuracy, bias, assumptions
  - Path: `./references/workflows/qa-review`
- **devil-review** — Adversarial stress-testing — bear case, attack vectors, failure modes
  - Path: `./references/workflows/devil-review`

### Content Creation

- **create-content** — Transform research into blog, X thread, TikTok script, YouTube script
  - Path: `./references/workflows/create-content`
- **create-image-prompt** — Generate AI image prompts optimized for DALL·E, Midjourney, Gemini, Flux
  - Path: `./references/workflows/create-image-prompt`

---

## MCP Data Sources

Optional data via MCP servers. Agent uses when available, skips gracefully when not.
Installation details: `./references/core/mcp-servers.md`

- **coingecko** — Real-time prices, market cap, volume, historical charts, 15k+ coins, 1000+ exchanges, onchain DEX data via GeckoTerminal
- **coinmarketcap** — Market data, rankings, metadata, global metrics, price conversions
- **defillama** — TVL, protocol revenue, yields, DEX volumes, stablecoin data, chain comparisons
- **dune** — Onchain SQL analytics, custom queries, protocol-level metrics
- **exa** — Neural web search, high-quality results for research depth
