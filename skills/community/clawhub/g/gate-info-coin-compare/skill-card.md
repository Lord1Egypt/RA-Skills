## Description:

Coin comparison. Use this skill whenever the user asks to compare two or more coins. Trigger phrases include: compare, versus, vs, which is better, difference. MCP tools: info_marketsnapshot_get_market_snapshot, info_coin_get_coin_info per coin (or batch/search when available).

This skill is ready for commercial/non-commercial use.

## Publisher:

[gate-exchange](https://clawhub.ai/user/gate-exchange)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to compare 2-5 cryptocurrencies side by side using public market snapshots, fundamentals, rankings, and optional technical signals. It produces a neutral, data-driven comparison report and avoids buy/sell recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat comparative crypto analysis as investment advice.

Mitigation: Keep the report informational, avoid buy/sell recommendations and price predictions, and include the skill's not-investment-advice disclaimer.

Risk: Unavailable or incomplete Gate Info MCP data could lead to misleading comparisons.

Mitigation: Confirm the Gate Info MCP integration is available, label missing dimensions as unavailable, and continue only with sourced public market, project, ranking, and technical data.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/gate-exchange/skills/gate-info-coin-compare)
- [Gate Info CoinCompare MCP Specification](artifact/references/mcp.md)
- [Gate Info Coin Compare Runtime Rules](artifact/references/gate-runtime-rules.md)
- [Info & News Common Runtime Rules](artifact/references/info-news-runtime-rules.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown comparison report with tables, concise analysis, risk warnings, and data availability notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses read-only Gate Info MCP data; output is informational and not investment advice.]

## Skill Version(s):

1.0.3 (source: server release metadata); packaged skill frontmatter reports 2026.4.6-1

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
