## Description: <br>
Generates a read-only crypto market overview from Gate Info MCP market, ranking, DeFi, macro, and news-event data for market-wide requests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gaixianggeng](https://clawhub.ai/user/gaixianggeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to answer broad crypto market-condition questions with a structured markdown briefing. Coin-specific, technical, risk, or deeper research requests are routed to specialized Gate skills. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Crypto market summaries may be mistaken for investment advice. <br>
Mitigation: Present outputs as informational market context, include the not-investment-advice disclaimer, and avoid buy, sell, or deterministic prediction language. <br>
Risk: Unavailable, stale, or partial MCP data can produce an incomplete market view. <br>
Mitigation: Label missing sections as unavailable, include data freshness where possible, and avoid fabricating metrics or events. <br>
Risk: Market-wide routing can be too broad for coin-specific, technical, risk, or deep research requests. <br>
Mitigation: Route those requests to the specialized Gate skills identified by the artifact instead of stretching the market overview workflow. <br>
Risk: The skill depends on the trust and availability of the Gate MCP server. <br>
Mitigation: Use it only with a trusted Gate MCP server and degrade gracefully when required tools are unavailable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gaixianggeng/gate-info-market-overview-staging) <br>
- [Gate Info MarketOverview MCP Specification](references/mcp.md) <br>
- [Gate Info Market Overview Runtime Rules](references/gate-runtime-rules.md) <br>
- [Info & News Common Runtime Rules](references/info-news-runtime-rules.md) <br>
- [Scenarios & Prompt Examples](references/scenarios.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown report with tables and short narrative sections] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only MCP-backed synthesis with timestamps, missing-data labels, and an informational-market-context disclaimer.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
