## Description:

FollowinMCP is an index and routing entry point for Followin MCP sub-skills covering crypto intelligence, sentiment, trading signals, macro dashboards, morning briefs, and U.S. stock analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rayniubi](https://clawhub.ai/user/rayniubi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent developers use this skill to route market-intelligence requests to the appropriate Followin MCP sub-skill. It supports workflows for crypto news, token sentiment, Telegram channel intelligence, trading signals, macro analysis, daily briefs, earnings review, and stock divergence scans.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary flags unsafe API-key placement in SSE URLs.

Mitigation: Use Followin API keys only through headers or a protected secret store, and avoid placing keys in URLs.

Risk: The security summary notes that saved watchlists can be used automatically in remote requests.

Mitigation: Disable saved watchlist use or require confirmation before sending watchlist tickers to Followin.

Risk: Broad market or Telegram wording may route a request into specialized remote data workflows.

Mitigation: Confirm the selected sub-skill and remote data scope before running workflows that could disclose user intent or market interests.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/rayniubi/skills/followin-mcp)
- [Followin Agent Skills README](references/README.md)
- [Followin Intel Center](references/01-followin-intel-center.SKILL.md)
- [Breaking News](references/02-breaking-news.SKILL.md)
- [Trending News Topics](references/03-trending-news-topics.SKILL.md)
- [Crypto Daily Brief](references/04-crypto-daily-brief.SKILL.md)
- [Token Buzz Views](references/05-token-buzz-views.SKILL.md)
- [Trading Strategy Signal](references/06-trading-strategy-signal.SKILL.md)
- [TG Channel Intel](references/07-tg-channel-intel.SKILL.md)
- [BTC Macro Dashboard](references/08-btc-macro-dashboard.SKILL.md)
- [Gold Macro Dashboard](references/09-gold-macro-dashboard.SKILL.md)
- [Macro Morning Brief](references/10-macro-morning-brief.SKILL.md)
- [US Stock Earnings Report](references/11-us-stock-earnings-report.SKILL.md)
- [Macro Analyzer](references/12-macro-analyzer.SKILL.md)
- [US Stock Divergence Scan](references/13-us-stock-divergence-scan.SKILL.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, configuration]

**Output Format:** [Markdown/text routing guidance with MCP configuration snippets and market-intelligence response structures]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Routes user intent across 13 sub-skills and may rely on Followin MCP or premium MCP services when the user has configured access.]

## Skill Version(s):

1.0.0 (source: server release metadata and OpenClaw metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
