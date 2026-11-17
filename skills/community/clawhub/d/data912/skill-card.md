## Description:

Queries Data912 market data endpoints for Argentina and USA instruments, including MEP/CCL quotes, market panels, historical OHLC series, option chains, and volatility metrics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ferminrp](https://clawhub.ai/user/ferminrp)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to retrieve and summarize public Data912 market data snapshots, historical OHLC series, option chains, and volatility metrics. The skill is intended for educational, non-real-time market data interpretation and not financial recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled OpenAPI reference includes an unrelated /contact operation outside the market-data behavior.

Mitigation: Do not invoke /contact for this skill; remove or isolate that operation from the reference spec before treating the release as low risk.

Risk: Shell-based query examples can be unsafe or unreliable when ticker input is not strictly validated.

Mitigation: Validate ticker symbols against the intended endpoint's accepted symbols and prefer non-shell HTTP usage or safely quoted, fixed URL construction.

Risk: Market data may be mistaken for real-time trading information.

Mitigation: State that Data912 data is educational and non-real-time, and avoid financial recommendations.

## Reference(s):

- [OpenAPI Specification](references/openapi-spec.json)
- [Data912 API](https://data912.com)
- [ClawHub Skill Page](https://clawhub.ai/ferminrp/skills/data912)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown summaries with optional inline shell commands and JSON excerpts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes educational/non-real-time data caveats and avoids trading advice.]

## Skill Version(s):

1.0.0 (source: server release metadata and user changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
