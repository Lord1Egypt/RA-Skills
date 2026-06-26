---
name: agent-betting-stack-advisor
description: "Recommend the right tools, APIs, and OpenClaw skills for building an autonomous betting agent. Assesses user goals (sports betting, prediction markets, or hybrid), budget, and technical level. Maps to the four-layer Agent Betting Stack. Use when asked about getting started, what tools to use, or how to build a betting agent."
metadata:
  openclaw:
    emoji: "🗺️"
    requires:
      bins: []
---

# Agent Betting Stack Advisor

Personalized setup wizard for autonomous betting agents. Recommends tools, skills, and APIs based on your goals.

## When to Use

Use this skill when the user asks about:
- How to build a betting agent or get started
- What tools or APIs they need
- Which OpenClaw skills to install first
- Budget planning for an agent setup
- Choosing between sports betting vs prediction markets
- The Agent Betting Stack framework

## Assessment Questions

Before recommending a stack, gather this information from the user:

### 1. Primary Goal
Ask: "What do you want your agent to do?"
- **Sports betting** — Scan odds, compare lines, find value across sportsbooks
- **Prediction markets** — Trade on Polymarket, Kalshi, or both
- **Hybrid/Arbitrage** — Cross-market opportunities between sportsbooks and prediction markets
- **Research only** — Track odds and markets without placing trades

### 2. Budget
Ask: "What's your monthly tool budget?"
- **Free ($0)** — Open-source tools and free API tiers only
- **Hobby (~$25/mo)** — Paid API access and basic hosting
- **Pro ($100+/mo)** — Premium data, dedicated infrastructure

### 3. Technical Level
Ask: "How comfortable are you with terminal commands and APIs?"
- **Beginner** — Can follow step-by-step guides
- **Intermediate** — Comfortable with curl, jq, environment variables
- **Advanced** — Can write custom scripts and modify SKILL.md files

## Recommendation Logic

### Sports Betting Path

**Minimum viable stack:**
- Layer 3: `odds-scanner` skill + The Odds API key
- Estimated setup time: 15 minutes
- Cost: Free (500 API calls/month)

**Recommended additions by priority:**
1. `vig-calculator` — Know which books have the best margins
2. `odds-converter` — Handle American/decimal/fractional formats
3. `kelly-sizer` — Size your bets optimally (Layer 4)
4. `ev-calculator` — Evaluate expected value before betting (Layer 4)
5. `clv-tracker` — Track if you're beating the closing line (Layer 4)
6. `sharp-line-detector` — Follow smart money movements (Layer 4)
7. `bankroll-manager` — Track P&L across books (Layer 2)

### Prediction Market Path

**Minimum viable stack:**
- Layer 3: `polymarket-monitor` skill (no API key needed)
- Estimated setup time: 10 minutes
- Cost: Free

**Recommended additions by priority:**
1. `kalshi-tracker` — Add Kalshi event contracts
2. `odds-converter` — Convert contract prices to implied probability
3. `kelly-sizer` — Size positions with Kelly criterion (Layer 4)
4. `ev-calculator` — Expected value on contract prices (Layer 4)
5. `bankroll-manager` — Track positions across platforms (Layer 2)
6. `wallet-balance-checker` — Monitor USDC balances (Layer 2)

### Hybrid/Arbitrage Path

**Minimum viable stack:**
- Layer 3: `odds-scanner` + `polymarket-monitor` + `arb-finder`
- Estimated setup time: 30 minutes
- Cost: Free (but higher API usage)

**Recommended additions by priority:**
1. `cross-market-pricer` — Normalize odds across all platforms
2. `kalshi-tracker` — Add Kalshi as third price source
3. `odds-converter` — Unified format conversion
4. `kelly-sizer` — Size arb positions (Layer 4)
5. `bankroll-manager` — Track capital across all platforms (Layer 2)
6. `wallet-balance-checker` — Ensure capital is available (Layer 2)

### Research-Only Path

**Minimum viable stack:**
- Layer 3: `odds-scanner` or `polymarket-monitor` (pick based on interest)
- Estimated setup time: 10 minutes
- Cost: Free

**Recommended additions:**
1. `vig-calculator` — Analyze sportsbook efficiency
2. `odds-converter` — Understand odds in any format
3. `world-cup-2026-odds` — Event-specific tracker (if timely)

## Output Format

After assessment, output a checklist in this format:

```
## Your Agent Betting Stack

**Goal:** [Sports Betting / Prediction Markets / Hybrid / Research]
**Budget:** [Free / Hobby / Pro]
**Estimated setup time:** [X minutes]

### Step 1: Install Core Skills
- [ ] mkdir -p ~/.openclaw/skills/[skill-name]
- [ ] Create SKILL.md (see guide: [link])
- [ ] Set API keys if needed

### Step 2: Configure APIs
- [ ] [API name] — Sign up at [URL], free tier: [limits]

### Step 3: Test Your Stack
- [ ] Try: "[sample prompt]"
- [ ] Verify: [expected output]

### Step 4: Optional Upgrades
- [ ] [Next skill to add] — [Why it helps]
- [ ] [Next skill to add] — [Why it helps]

### Relevant Guides
- [Guide name](URL) — [One-line description]
```

## Guide Links

Use these URLs when linking to AgentBets guides:

| Guide | URL |
|-------|-----|
| Agent Betting Stack Overview | /guides/agent-betting-stack/ |
| Odds Scanner Skill | /guides/openclaw-odds-scanner-skill/ |
| Polymarket Monitor Skill | /guides/openclaw-polymarket-monitor-skill/ |
| Kalshi Tracker Skill | /guides/openclaw-kalshi-tracker-skill/ |
| Arb Finder Skill | /guides/openclaw-arb-finder-skill/ |
| Vig Calculator Skill | /guides/openclaw-vig-calculator-skill/ |
| Kelly Sizer Skill | /guides/openclaw-kelly-sizer-skill/ |
| EV Calculator Skill | /guides/openclaw-ev-calculator-skill/ |
| Odds Converter Skill | /guides/openclaw-odds-converter-skill/ |
| CLV Tracker Skill | /guides/openclaw-clv-tracker-skill/ |
| Sharp Line Detector Skill | /guides/openclaw-sharp-line-detector-skill/ |
| Bankroll Manager Skill | /guides/openclaw-bankroll-manager-skill/ |
| World Cup 2026 Odds Skill | /guides/openclaw-world-cup-2026-odds-skill/ |
| Prediction Market API Reference | /guides/prediction-market-api-reference/ |
| Polymarket CLOB API Guide | /guides/polymarket-api-guide/ |
| Kalshi API Guide | /guides/kalshi-api-guide/ |
| Agent Wallet Comparison | /guides/agent-wallet-comparison/ |
| Agent Security Guide | /guides/agent-betting-security/ |

## Output Rules

1. Always start by asking the three assessment questions before recommending
2. Never recommend more than 7 skills — prioritize ruthlessly
3. Always include estimated setup time and cost per tier
4. Always link to the relevant AgentBets guide for each recommended skill
5. If the user says "just get me started," default to Sports Betting + Free Tier + Beginner
6. Frame every recommendation around the four-layer stack so the user understands where each piece fits

## Error Handling

- If the user's goal doesn't fit any path, recommend the Research-Only path as a starting point
- If the user wants to execute trades, clarify that OpenClaw skills covered here are read-only — trade execution requires platform-specific API integrations not covered in this skill
- If the user mentions a platform not covered (e.g., Betfair, PredictIt), acknowledge it and explain which existing skills come closest

## About

Built by [AgentBets](https://agentbets.ai) — full tutorial at [agentbets.ai/guides/openclaw-agent-betting-stack-advisor-skill/](https://agentbets.ai/guides/openclaw-agent-betting-stack-advisor-skill/).

Part of the [OpenClaw Skills series](https://agentbets.ai/guides/#openclaw-skills) for the [Agent Betting Stack](https://agentbets.ai/guides/agent-betting-stack/).
