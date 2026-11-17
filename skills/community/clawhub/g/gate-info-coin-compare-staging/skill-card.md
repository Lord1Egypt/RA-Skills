## Description:

Compares two to five cryptocurrency assets using Gate Info market snapshots, fundamentals, rankings, and optional technical signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gaixianggeng](https://clawhub.ai/user/gaixianggeng)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to compare crypto assets side by side across market performance, fundamentals, liquidity, technical indicators, and differentiated risks. Outputs are informational analysis and should not be treated as investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may mistake comparative crypto analysis for investment advice.

Mitigation: Keep outputs data-driven, avoid buy or sell recommendations and price predictions, and include an informational-analysis disclaimer.

Risk: Ambiguous symbols, missing MCP tools, or partial tool failures can produce incomplete comparisons.

Mitigation: Clarify ambiguous coin identities, verify Gate Info MCP availability, and label missing or failed dimensions as unavailable instead of fabricating data.

Risk: Market, liquidity, and technical data can change quickly.

Mitigation: Use consistent time windows, report source/update timing when available, and frame conclusions as point-in-time comparisons.

## Reference(s):

- [Gate Info CoinCompare MCP Specification](references/mcp.md)
- [Gate Info Coin Compare Runtime Rules](references/gate-runtime-rules.md)
- [Info & News Common Runtime Rules](references/info-news-runtime-rules.md)
- [ClawHub Skill Page](https://clawhub.ai/gaixianggeng/skills/gate-info-coin-compare-staging)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown tables with concise comparative analysis and risk notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Gate Info MCP availability; marks missing data as unavailable and avoids buy, sell, or price-prediction recommendations.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter reports 2026.4.6-1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
