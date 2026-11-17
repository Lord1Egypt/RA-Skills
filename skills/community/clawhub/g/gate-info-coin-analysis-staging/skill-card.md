## Description:

Provides a read-only, single-coin cryptocurrency analysis workflow that combines fundamentals, market data, technical indicators, news, and social sentiment into a structured report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gaixianggeng](https://clawhub.ai/user/gaixianggeng)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to request a neutral, data-driven analysis of one cryptocurrency when they need fundamentals, market context, technical signals, recent news, and social sentiment in one report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cryptocurrency analysis can be mistaken for investment advice or trading instructions.

Mitigation: Keep the report neutral and data-driven, include a non-investment-advice disclaimer, and avoid explicit buy, sell, or target-price recommendations.

Risk: Unavailable or partial MCP data could make the analysis misleading.

Mitigation: Degrade gracefully, label unavailable sections clearly, and never fabricate missing fundamentals, technicals, news, or sentiment data.

Risk: Ambiguous coin names or multi-dimension requests can route the agent to the wrong workflow.

Mitigation: Ask the user to clarify ambiguous coin symbols and route comparisons, risk-only checks, event attribution, or broader research requests to the appropriate Gate skill.

## Reference(s):

- [Gate Info CoinAnalysis MCP Specification](references/mcp.md)
- [Gate Info Coin Analysis Runtime Rules](references/gate-runtime-rules.md)
- [Info & News Common Runtime Rules](references/info-news-runtime-rules.md)
- [ClawHub skill page](https://clawhub.ai/gaixianggeng/skills/gate-info-coin-analysis-staging)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown report with tables, bullet lists, linked news items, risk warnings, and a non-investment-advice disclaimer.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses available read-only Gate Info and Gate News MCP data; unavailable dimensions are labeled instead of fabricated.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
