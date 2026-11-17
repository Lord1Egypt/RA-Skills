## Description:

Cn Stock Brief generates Chinese-language A-share market briefs from Eastmoney public market data, including major indices, sector performance, and top gainers and losers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[freedompixels](https://clawhub.ai/user/freedompixels)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, market analysts, and agents use this skill to fetch current Chinese A-share market data and produce concise Chinese daily market briefs or JSON snapshots for downstream workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes live requests to Eastmoney for public market data, so output depends on third-party availability and current market data quality.

Mitigation: Treat unavailable or incomplete responses as data-source limitations and verify important market information against an authoritative source before acting.

Risk: The generated market brief may be mistaken for investment advice.

Mitigation: Use the report for informational purposes only and keep the skill's stated non-advice disclaimer visible in downstream use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/freedompixels/skills/cn-stock-brief)
- [Eastmoney public market data endpoint](https://push2.eastmoney.com/)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [Chinese plain text market brief or JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Optional CLI modes include --json, --indices, and --sectors.]

## Skill Version(s):

1.2.7 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
