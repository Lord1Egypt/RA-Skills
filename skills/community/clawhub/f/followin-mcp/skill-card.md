## Description: <br>
Routes agent requests to Followin MCP sub-skills for crypto intelligence, market sentiment, trading signals, macro dashboards, and U.S. stock analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rayniubi](https://clawhub.ai/user/rayniubi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to select the right Followin MCP sub-skill for finance and crypto intelligence tasks, then follow that sub-skill's routing boundaries and tool mapping. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API keys may be exposed if placed in URL query strings. <br>
Mitigation: Prefer secret storage or header-only authentication when supported, and avoid sharing or logging MCP configuration that contains query-string credentials. <br>
Risk: Broad market prompts can trigger multiple external finance and crypto queries, including premium endpoints that may cost money or reveal research intent. <br>
Mitigation: Ask for scope clarification before broad market requests and confirm use of premium data sources when cost or privacy matters. <br>


## Reference(s): <br>
- [FollowinMCP ClawHub release](https://clawhub.ai/rayniubi/followin-mcp) <br>
- [Followin sub-skill index](references/README.md) <br>
- [Followin Intel Center](references/01-followin-intel-center.SKILL.md) <br>
- [Breaking News Analysis](references/02-breaking-news.SKILL.md) <br>
- [Trending News Topics](references/03-trending-news-topics.SKILL.md) <br>
- [Crypto Daily Brief](references/04-crypto-daily-brief.SKILL.md) <br>
- [Token Buzz Views](references/05-token-buzz-views.SKILL.md) <br>
- [Trading Strategy Signal](references/06-trading-strategy-signal.SKILL.md) <br>
- [TG Channel Intel](references/07-tg-channel-intel.SKILL.md) <br>
- [BTC Macro Dashboard](references/08-btc-macro-dashboard.SKILL.md) <br>
- [Gold Macro Dashboard](references/09-gold-macro-dashboard.SKILL.md) <br>
- [Macro Morning Brief](references/10-macro-morning-brief.SKILL.md) <br>
- [US Stock Earnings Report](references/11-us-stock-earnings-report.SKILL.md) <br>
- [Macro Analyzer](references/12-macro-analyzer.SKILL.md) <br>
- [US Stock Divergence Scan](references/13-us-stock-divergence-scan.SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, configuration] <br>
**Output Format:** [Markdown guidance with MCP configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Routes requests to referenced sub-skills; some sub-skills call external Followin MCP or premium MCP services.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and OpenClaw metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
