## Description:

Fetches public Eastmoney industry and concept sector snapshots for China A-share market context.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luyao-inc](https://clawhub.ai/user/luyao-inc)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to gather a current, public-source sector snapshot for China A-share market analysis. The output is informational market context only and is not investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill returns market information that could be mistaken for investment advice.

Mitigation: Treat outputs as informational context only and require independent review before any trading or allocation decision.

Risk: Public market-data endpoints can be unavailable, incomplete, delayed, or restricted.

Mitigation: Check the returned ok/detail fields and verify important values against authoritative market-data sources before relying on them.

Risk: The skill runs a local Python script that makes outbound requests to public Eastmoney endpoints.

Mitigation: Review the script before installation and run it only in environments where outbound public market-data requests are permitted.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/luyao-inc/skills/china-stock-sector-strategy)
- [Eastmoney Public Market Data Endpoint](https://push2.eastmoney.com/)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [JSON returned by a local Python command, with agent-facing guidance in Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns ok, payload, sectors_count, concepts_count, operation, period_type, and source fields; uses public data endpoints without cookies or trading-account access.]

## Skill Version(s):

2.0.0 (source: release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
