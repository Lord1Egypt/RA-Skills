---
name: domain-keyword-intelligence
description: Discover domain investment opportunities from emerging keyword spikes. Filters junk signals from real multi-party market activity using registration profiling, catalyst research, and NRDS position analysis. Powered by DomainKits MCP.
homepage: https://domainkits.com/mcp
metadata: {"openclaw":{"emoji":"📈","primaryEnv":"DOMAINKITS_API_KEY"}}

---

# Domain Keyword Intelligence

Spot domain market trends before they peak. This skill transforms raw keyword spike data into actionable investment signals by separating real multi-party demand from single-operator noise.

## Why This Skill?

Raw `keywords_trends(emerging)` data typically returns 50-100 keywords — most are junk. This skill's value is extracting signal from noise:

- **Profile every spike** — Is it "one person" bulk-registering, or a genuine multi-party market?
- **Research the catalyst** — What news, product launch, or domain sale is driving registrations?
- **Analyze positioning** — How are registrants combining this keyword? Where are the gaps?

## Setup

### Prerequisites

This skill requires the **DomainKits MCP** connection and access to **web_search**.

- **DomainKits MCP**: Provides `keywords_trends`, `nrds`, and other domain intelligence tools
- **web_search**: Platform built-in tool, used for mandatory catalyst research

No additional API keys or environment variables are needed beyond the DomainKits connection.

### Option 1: Claude.ai / OpenClaw

Connect DomainKits via Settings → Connectors. The platform handles authentication automatically.

### Option 2: Claude Code / MCP Config

Add to your MCP config:
```json
{
  "mcpServers": {
    "domainkits": {
      "baseUrl": "https://api.domainkits.com/v1/mcp"
    }
  }
}
```

With API key (for higher limits):
```json
{
  "mcpServers": {
    "domainkits": {
      "baseUrl": "https://api.domainkits.com/v1/mcp",
      "headers": {
        "X-API-Key": "$env:DOMAINKITS_API_KEY"
      }
    }
  }
}
```

Get your API key at https://domainkits.com

## Tools Used

This skill orchestrates the following tools:

- `keywords_trends` — Fetch emerging keyword spikes (DomainKits MCP)
- `nrds` — Search newly registered domains by keyword and position (DomainKits MCP)
- `web_search` — Investigate catalysts behind registration spikes (platform built-in)

Optional follow-up tools (user-driven):
- `deleted` — Recently dropped domains
- `expired` — Backorderable domains
- `aged` — Domains listed for sale
- `keyword_intel` — Deep keyword analysis
- `domain_generator` — Creative name ideas

## Instructions

### Step 1: Fetch Emerging Keyword Data

Call `keywords_trends(type="emerging")` to get keywords with registration volume spikes in the last 7-14 days. The tool returns per-keyword data including registration volume (w3/w4), com_ratio, forsale_pct, might_use_count, top_registrar, and other dimensions needed for Step 2 analysis.

### Step 2: Multi-Dimensional Profile Analysis (Core Logic)

#### How the domain market works

The domain market is a multi-party ecosystem. After registering a domain, a person can only do one of three things with it:

1. **Sell it** — list on aftermarket platforms and wait for buyers. This is investor behavior. Their presence shows up in `forsale_pct`.

2. **Use it (maybe)** — point it to infrastructure (Cloudflare, AWS, Vercel). Their presence shows up in `might_use_count` — but this only indicates the domain was configured beyond default parking, not that it is genuinely in use. It could be a real project or a site farm. Only meaningful when registrar distribution is diverse.

3. **Unknown** — the domain sits on default NS, neither listed for sale nor pointed to any infrastructure. The registrant's intent is unclear. This is the remainder after subtracting forsale and might_use from total registrations.

These three states account for every registered domain. Like any financial market, a healthy keyword market requires **liquidity** — active trading, not just ownership.

`forsale_pct` is the market's trading volume. If forsale is very low, market participation is low — this is not a healthy market signal. A keyword with high com_ratio, dispersed registrars, and high might_use_count but near-zero forsale has registrations but no market.

Two hard rules:
- **If forsale is below 3%, discard.** Do not explain it away with "end-user driven" or "terminal demand" — low forsale means low market participation, period.
- **Never make recommendations or judgments without data.** Labels like "NFL-related", "Chinese pinyin demand", "gaming keyword" are speculation unless confirmed by web_search. If you have not searched, do not guess. Output data only, not narratives. Potential healthy keywords must be verified through NRDS registration analysis (Step 3) before being presented as opportunities.

Two cross-cutting dimensions apply to all three participant types:

- **`com_ratio`** — the "blue chip ratio." High com_ratio means participants are investing in .com — the most expensive TLD. Low com_ratio means activity is concentrated on cheap TLDs.

- **`top_registrar.pct`** — the "exchange concentration." Registrars are channels, not identity labels. High concentration (e.g., above 80%) on a single registrar reduces confidence that many independent parties are involved. A real multi-party market almost always shows distributed registrar usage.

**The core question for every keyword is: Is this data from "one person" or "a market"?**

When analyzing a keyword, check whether each participant type is present. When a type is absent, ask why — the answer tells you what's really happening. When a type overwhelmingly dominates, ask whether that makes sense for a real market or whether it points to a single operator.

#### Filtering Process

1. Calculate w4/w3 growth rate for each keyword
2. Profile each keyword across all dimensions — check whether all three participant types are present and whether the two cross-cutting dimensions are reasonable
3. Classify as `junk` (single operator or missing participant roles) or `healthy` (genuine multi-party market)
4. Sort healthy keywords by w4/w3 growth rate
5. Take Top 5-8 for deep analysis

#### Output Format

Summarize filtering results concisely:
- N total emerging keywords
- Excluded X junk signals — each in under 10 words (e.g., "ethereum: single registrar, all forsale, no .com")
- Identified Z healthy market signals

List healthy keywords with key profile data:
```
llm — W3: 794 → W4: 979 (↑23%)
  com_ratio: 82.6% | forsale: 36.8% | might_use: 63 | top_registrar: Unstoppable Domains 29.7%
  Profile: Multi-party participation, .com dominant, mix of investment and usage. Healthy signal.
```

### Step 2.5: Catalyst Research (web_search MANDATORY)

For each healthy keyword identified in Step 2, use `web_search` to investigate what is driving the registration spike. Domain registration spikes are predominantly driven by technology and internet industry events — product launches, AI model releases, platform announcements, viral open-source projects, regulatory changes, major acquisitions, or high-profile domain sales.

Profile analysis tells you WHETHER a signal is healthy. Catalyst research tells you WHY — and "why" determines whether the opportunity is worth pursuing.

For each healthy keyword, search with a technology lens. Prioritize the last 3 days — emerging spikes are almost always driven by very recent events. If nothing is found within 3 days, extend to 10 days maximum:
1. `{keyword} news` — look for product launches, funding rounds, open-source projects, platform announcements, regulatory changes
2. `{keyword} domain sold price` — a high-value domain sale is the single strongest catalyst for registration spikes

#### Output: Catalyst Verification Table

Present catalyst findings as this table. The Source column must contain a real URL from web_search results. No URL = keyword does not appear in the table. Do not substitute with training data.
```
| Keyword | W4 | forsale% | Catalyst | Source |
|---------|-----|---------|----------|--------|
| molt    | 576 | 17.2%   | OpenClaw/Moltbot AI agent project | [CNBC](url) |
| nemo    | 374 | 29.7%   | Nvidia NeMo/NemoClaw, GTC 2026 | [TradingView](url) |
| llm     | 768 | 28.6%   | PrivateLLM.com sold $250K | [DomainInvesting](url) |
```

Rules:
- Source = actual URL from web_search. Not training data.
- No catalyst found AND no URL → keyword excluded from table. Note "no catalyst identified" in the filtering summary and move on.
- forsale < 3% → never reaches this table (killed at Step 2).
- Only keywords in this table proceed to Step 3.

### Step 3: NRDS Registration Position Analysis

**This step bridges "macro trend" to "micro execution."**

For each healthy keyword, call `nrds` to examine actual registration patterns:
```
nrds(keyword="<keyword>", position="start", tld="com", no_hyphen="true", sort="reg_date_desc", days_range="0-10")
nrds(keyword="<keyword>", position="end", tld="com", no_hyphen="true", sort="reg_date_desc", days_range="0-10")
```

#### Analysis Points

1. **Position distribution**:
   - `position=start` (e.g., llmtools.com, llmagent.ai) → keyword as category anchor
   - `position=end` (e.g., myllm.com, bestllm.io) → keyword as modifier
   - Comparing volumes reveals how the market positions this keyword

2. **Popular combinations**: Extract high-frequency combination words from registrations. E.g., llm + agent, llm + chat, llm + tools. These represent the market's view on the keyword's most valuable applications

3. **Registration quality**:
   - Length distribution (short names taken = fierce competition; short names available = window open)
   - `period` (registration term): 6+ years = serious project, 1 year = speculative trial
   - `prefix_tld_count`: high = prefix registered across many TLDs = strong recognition

4. **Investor vs end-user behavior**:
   - NS: afternic.com / sedo.com / thisdomain.forsale = investor listing
   - NS: cloudflare / aws / vercel = domain configured for use (could be real project or site farm — check if naming patterns are diverse or template-like)
   - Ratio reveals speculation phase vs adoption phase

#### Output Format
```
llm — NRDS Registration Analysis
  position=start: 287 domains (llmtools, llmagent, llmchat, llmcode...)
  position=end: 143 domains (myllm, bestllm, openllm, smartllm...)
  Popular combos: agent (42), tools (28), chat (23), code (19), hub (15)
  Market direction: Heavy llm+agent combinations suggest bullish sentiment on LLM Agent space
  Quality: Short domains (<10 char) largely taken, 10-15 char range still has room
```

### Step 4: Next Steps

After presenting the trend analysis and NRDS findings, let the user know they can use DomainKits' other tools to explore domain opportunities for any keyword that interests them — such as `deleted` for recently dropped domains, `expired` for backorderable domains, `aged` for domains listed for sale, `keyword_intel` for deep keyword analysis, or `domain_generator` for creative name ideas. Let the user choose which keywords and directions to pursue.

## Output Rules

- **Language**: Follow user's language
- **Concise**: Profile judgments in one sentence. Skip junk quickly, expand on healthy signals
- **Data-driven**: Every judgment cites specific numbers
- **Honest**: No catalyst found → say "cause unidentified" — never fabricate
- **Quota-aware**: Step 3 consumes many tool calls. Show Step 2 results first and let user pick 2-3 keywords before continuing

## Access Tiers

Guest users can use this skill with limited daily search quota. Register a free account at https://domainkits.com to unlock higher search limits and access to all tools.

## Privacy

- Works without API key (guest tier)
- No user data stored by this skill
- DomainKits: GDPR compliant, memory OFF by default

## Links

- DomainKits: https://domainkits.com/mcp
- GitHub: https://github.com/ABTdomain/domainkits-mcp
- Contact: info@domainkits.com
- Developed by: https://abtdomain.com