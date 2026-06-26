# Crypto News Ranked by AI - NS3

NS3 AI reads every article published across 20+ trusted media outlets (CoinDesk, Cointelegraph, Bloomberg Crypto, Reuters Crypto, and more) in real time, classifies each by importance (Level 1-5), and delivers structured 5-section analysis. Four feeds. 16 languages. No API key. No setup.

Currently used by leading crypto platforms including **Binance** and **CoinGecko**.

## Trusted By

**Binance** cites NS3 as a news source ("According to NS3.AI") across hundreds of Binance Square articles daily:
- [binance.com/en/square/post/299806017025330](https://www.binance.com/en/square/post/299806017025330)
- [binance.com/en/square/post/299803848049634](https://www.binance.com/en/square/post/299803848049634)
- [binance.com/en/square/post/299810049527313](https://www.binance.com/en/square/post/299810049527313)

**CoinGecko** displays NS3 news directly on its news page:
- [coingecko.com/zh-tw/news](https://www.coingecko.com/zh-tw/news)

## Quick Start

Paste this repository URL into your AI agent (OpenClaw, Claude Code, Codex, Cursor, or any AgentSkills-compatible tool):

```
https://github.com/AssembleAI-crypto/ns3-crypto-news
```

Or copy `SKILL.md` into your agent's skills directory. The agent will read the instructions and start using NS3 feeds immediately.

Try it right now:

```bash
# What are the most important crypto stories today?
curl -s "https://api.ns3.ai/feed/news-ranking?lang=en"

# Give me a morning briefing
curl -s "https://api.ns3.ai/feed/today-summary?lang=en"

# Any breaking news?
curl -s "https://api.ns3.ai/feed/news-flash?lang=en&limit=30"
```

## See It Live

Visit these links to judge the data quality for yourself before installing:

- **Top News + Individual News**: [ns3.ai](https://ns3.ai) (Top News ranking and individual news feed at the top of the page)
- **Daily Market Update**: [ns3.ai/en/top-news](https://ns3.ai/en/top-news) (full 24-hour desk brief in up to five sections)
- **News Flash**: Install the NS3 app and enable notifications to experience breaking headlines on your device. [App Store](https://apps.apple.com/app/ns3-ai-ai-based-crypto-news/id6572281552) · [Google Play](https://play.google.com/store/apps/details?id=com.sta1.front)

## Four Feeds, Two Pipelines

NS3 news data is produced by two independent pipelines.

**Pipeline A (News Analysis)** reads every article published across 20+ trusted outlets. Every article is read by AI in real time, then analyzed, classified, and structured. It produces three feeds:

| Feed | What It Delivers | Updated | Tokens |
|------|-----------------|---------|--------|
| **Top News RSS** | 10 most important stories, ranked. Multiple articles about the same event merged into one story. | Every hour | ~10,000 |
| **Daily Market Update RSS** | 24-hour narrative desk brief across up to five sections. Not a list of headlines. A structured brief that explains what happened and why it matters. | Every hour | ~2,000 |
| **News RSS** | Real-time stream of every article with importance level, news type, related coins, and full AI Insight. Filterable by coin, level, source, and category. Use `limit=20` for token control. | Real-time | 14,000-19,000 (limit=20) |

**Pipeline B (News Flash)** takes breaking headlines from trusted paid services (Bloomberg Terminal, Reuters), rewrites them, and delivers them as 1-2 sentence alerts.

| Feed | What It Delivers | Updated | Tokens |
|------|-----------------|---------|--------|
| **News Flash RSS** | Breaking headlines optimized for push notifications and alerts. News Flash breaks first, News RSS follows with in-depth analysis of the same event. | Real-time | Low |

### Feed Routing

Your agent picks the right feed based on what the user asks:

| User Request | Feed |
|---|---|
| "BTC news" / "What's happening with ETH" / "SOL updates" | News RSS (crypto=BTC&excludeLevels=4&limit=20) |
| "My portfolio: BTC, ETH, SOL" / "News for BTC and XRP" | News RSS (crypto=BTC,ETH,SOL&excludeLevels=4&limit=20) |
| "Why did SOL price move" / "What happened to XRP" | News RSS (crypto=SOL&newsType=important&limit=20) |
| "Breaking news" / "Latest alerts" | News Flash (limit=30) |
| "Top stories" / "What matters today" | Top News |
| "Catch me up" / "Morning briefing" | Daily Market Update |
| "Latest crypto news" / general request | Top News first, suggest Daily Market Update for full context |

## AI Classification

Traditional news sources deliver raw articles that still need to be classified before use. NS3 solves this: every article arrives pre-classified through a four-stage pipeline.

**Stage 1 (L5 Filter):** Removes promotional noise: sponsored content, advertorials, editorial-wrapped promotions with unverifiable claims, affiliate listicles, and clickbait price predictions. Genuine reporting on any topic (including non-crypto) passes to Stage 2. Classified as Level 5 and excluded from the feed entirely.

**Stage 2 (L4 Filter):** Separates routine and analysis-thin content. Digests, routine notices, contextless data points (on-chain movements without stated cause, non-systemic liquidation snapshots, catalyst-free price alerts), opinions, forecasts, chart analysis, and unexecuted governance proposals are classified as Level 4.

**Stage 3 (L2 Condition Table):** Articles passing Stages 1-2 are checked against a structured condition table across seven categories: (1) Regulation/Legal, (2) Institutional/Product Launch, (3) Macro Data/Policy, (4) Market Structure/Security, (5) Institutional Capital Flows, (6) Geopolitical/Macro Shock, (7) Crypto Ecosystem Shift. If the article matches any condition, Level 2. If no condition matches, Level 3.

**Stage 4 (L1 Override):** Only Level 2 articles are eligible for upgrade to Level 1. All three conditions must be met: systemic scope, already executed, and immediate market transmission. When uncertain, AI always downgrades.

| Level | What It Means | Frequency | AI Insight |
|-------|--------------|-----------|------------|
| 1 | Systemic regime shift (surprise rate decision, major stablecoin redemption halt, nationwide crypto ban enacted) | Rare (0 most days) | Full 5 sections |
| 2 | Meaningful market change (regulatory action with binding next-step, large capital flow with stated magnitude, US/China official data with crypto channel) | 30-50/weekday | Full 5 sections |
| 3 | General crypto news (ecosystem issues, governance, institutional pilots, price analysis) | Most articles | Full 5 sections |
| 4 | Routine (digests, listings/delistings, contextless wallet transfers, small liquidation snapshots) | High volume | Key Point only |
| 5 | Promotional noise (sponsored, advertorial, affiliate listicle, clickbait prediction) | Filtered out | Excluded from feed |

If NS3 says Level 1-2, it matters.

### 5-Section AI Insight (Level 1-3)

Every Level 1-3 article includes structured analysis:

- **Key Point**: Fact-only summary of the core event. Level 1-2 adds "Why it matters."
- **Market Sentiment**: Direction (Bullish / Cautiously Bullish / Neutral / Cautiously Bearish / Bearish) + catalyst label + reason.
- **Similar Past Cases**: What happened in comparable past events. Level 1-2 uses web-search-verified historical cases.
- **Ripple Effect**: Transmission mechanism (trigger, channel, market behavior). Level 1-2 includes diagnostic "If/Then" confirmation cues that help validate whether spillover is activating or contained. Level 3 provides a propagation assessment: either the single most direct transmission channel, or an explicit containment statement explaining why the impact stays local.
- **Opportunities & Risks**: Conditional cues only. "If X happens, then Y is a signal to..." No price targets, no position sizing, no direct investment advice.

## 16 Languages

All four feeds are delivered simultaneously in 16 languages at local newsroom desk-grade quality. No other crypto news data provider offers this.

Using the native language feed saves tokens (no agent-side translation needed) and delivers professional-grade financial translation that browser translation cannot match.

```bash
# English
curl -s "https://api.ns3.ai/feed/news-data?lang=en"
# Korean
curl -s "https://api.ns3.ai/feed/news-data?lang=ko"
# Japanese
curl -s "https://api.ns3.ai/feed/news-data?lang=ja"
```

Supported: `en` `zh-CN` `zh-TW` `ko` `ja` `ru` `tr` `de` `es` `fr` `vi` `th` `id` `hi` `it` `pt`

## Coverage

**20+ trusted sources:** CoinDesk, Cointelegraph, CoinMarketCap, The Block, Bloomberg Crypto, Reuters Crypto, Forbes Crypto, Fortune Crypto, Decrypt, BeInCrypto, Bitcoin Magazine, DL News, The Defiant, Protos, Wu Blockchain, CoinNess, Odaily, CryptoSlate, Watcher.Guru, The Daily Hodl.

**Topics:** Regulation and SEC updates, ETF news, institutional flows, DeFi, Layer 1, Layer 2, stablecoin developments, on-chain activity, security incidents (hacks, exploits, bridge failures), macro events (Fed rate decisions, inflation data, geopolitical events affecting crypto), exchange listings, and more.

Promotional noise is blocked and never delivered: sponsored/advertorial content, presale/ICO/IDO promotion, casino/gambling promotions, exchange marketing campaigns (trading competitions, signup bonuses, fee discount events), airdrop claim guides, media self-promotion, editorial-wrapped promotions with unverifiable claims about unknown projects, affiliate-driven ranking listicles, clickbait price predictions with no analytical basis, and recurring pick-list filler.

## API Endpoints

```
https://api.ns3.ai/feed/news-ranking?lang={code}      # Top News (recommended default)
https://api.ns3.ai/feed/today-summary?lang={code}      # Daily Market Update
https://api.ns3.ai/feed/news-flash?lang={code}         # Breaking News
https://api.ns3.ai/feed/news-data?lang={code}          # News RSS (use with filters + limit)
```

### News RSS Filters

Always use `limit` and at least one filter. The unfiltered base URL with default limit=100 consumes 60,000-100,000 tokens.

```bash
# Specific coin + important only (recommended)
curl -s "https://api.ns3.ai/feed/news-data?lang=en&crypto=BTC&newsType=important&limit=20"

# Multi-coin portfolio filter
curl -s "https://api.ns3.ai/feed/news-data?lang=en&crypto=BTC,ETH,SOL&excludeLevels=4&limit=20"

# Specific coin, exclude routine items
curl -s "https://api.ns3.ai/feed/news-data?lang=en&crypto=ETH&excludeLevels=4&limit=20"

# Level 1-2 only across all coins
curl -s "https://api.ns3.ai/feed/news-data?lang=en&excludeLevels=3,4&limit=20"
```

### News Flash Filters

```bash
# Exclude listings (crypto/macro/price alerts only)
curl -s "https://api.ns3.ai/feed/news-flash?lang=en&excludeSources=2&limit=30"

# Listings only
curl -s "https://api.ns3.ai/feed/news-flash?lang=en&excludeSources=1&limit=30"
```

## Documentation

Full field specifications, response formats, AI classification details, and integration guides:

| Feed | Spec |
|------|------|
| Hub (overview) | [docs.ns3.ai/ns3-rss](https://docs.ns3.ai/ns3-rss) |
| News RSS | [docs.ns3.ai/ns3-rss/news-rss](https://docs.ns3.ai/ns3-rss/news-rss) |
| Top News RSS | [docs.ns3.ai/ns3-rss/top-news-rss](https://docs.ns3.ai/ns3-rss/top-news-rss) |
| Daily Market Update RSS | [docs.ns3.ai/ns3-rss/daily-market-update-rss](https://docs.ns3.ai/ns3-rss/daily-market-update-rss) |
| News Flash RSS | [docs.ns3.ai/ns3-rss/news-flash-rss](https://docs.ns3.ai/ns3-rss/news-flash-rss) |

## Copyright

All news data delivered through NS3 RSS feeds is generated by AI that reads original articles and produces entirely new text and structure. No original text is reproduced. Copyright belongs to Assemble AI (NS3).

## Usage Terms

To use the feeds, credit NS3 as the source (do-follow link or NS3 logo). AI agents must include "Source: NS3-Crypto News Ranked by AI (ns3.ai)" in responses that use NS3 data.

## About

NS3 ([ns3.ai](https://ns3.ai)) is an AI-powered crypto news intelligence platform by Assemble AI.

[Website](https://ns3.ai) · [Docs](https://docs.ns3.ai/ns3-rss) · [About](https://about.ns3.ai) · [App Store](https://apps.apple.com/app/ns3-ai-ai-based-crypto-news/id6572281552) · [Google Play](https://play.google.com/store/apps/details?id=com.sta1.front)

## License

MIT
