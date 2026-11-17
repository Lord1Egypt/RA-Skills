## Description:

A China A-share trading assistant that fetches market data, summarizes individual stocks and indices, identifies hot sectors, drafts trading strategy guidance, and helps track price alerts for Shanghai and Shenzhen A-share securities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xndks](https://clawhub.ai/user/xndks)

### License/Terms of Use:


## Use Case:

External users use this skill to research China mainland A-share stocks, market indices, sector momentum, trading ranges, stop-loss and take-profit levels, and price alerts. Outputs should support research and decision review, not replace professional financial advice.

### Deployment Geography for Use:

Global; market coverage is limited to China mainland A-share equities.

## Known Risks and Mitigations:

Risk: Trading suggestions may be interpreted as investment advice.

Mitigation: Treat outputs as research only, preserve risk disclosures, and require user or qualified reviewer judgment before any trade.

Risk: Market analysis may rely on unauthenticated or non-HTTPS data feeds.

Mitigation: Verify important prices and signals against trusted broker, exchange, or verified HTTPS data sources before acting.

Risk: Price alerts and watchlists may reveal sensitive trading interests.

Mitigation: Store alert data only with explicit user intent, keep it under user control, and remove it when it is no longer needed.

## Reference(s):

- [Analysis methods reference](references/analysis.md)
- [Data sources reference](references/data-sources.md)
- [ClawHub skill page](https://clawhub.ai/xndks/skills/a-stock-trading-assistant)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown analysis with concise tables, risk notes, shell command examples, and optional JSON data from the bundled fetch script.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stock and market outputs include data source and fetch time when available.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
