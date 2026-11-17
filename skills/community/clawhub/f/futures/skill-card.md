## Description:

Queries real-time and historical futures market data for Shanghai, Dalian, Zhengzhou, China Financial Futures, and Guangzhou futures exchanges using JisuAPI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jisuapi](https://clawhub.ai/user/jisuapi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to answer futures price, contract movement, exchange listing, and historical K-line questions for supported Chinese futures exchanges.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends JISU_API_KEY and requested exchange, contract, and date-range parameters to JisuAPI over the network.

Mitigation: Install only when JisuAPI is an acceptable data provider, provide the key through the JISU_API_KEY environment variable, and rotate or revoke the key if exposure is suspected.

Risk: Futures responses depend on third-party API availability, permissions, rate limits, and data freshness.

Mitigation: Surface returned timestamps and error objects to users, and verify consequential trading or compliance decisions against authoritative market sources.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jisuapi/skills/futures)
- [JisuAPI Website](https://www.jisuapi.com/)
- [JisuAPI Futures API Documentation](https://www.jisuapi.com/api/futures/)
- [JisuAPI Futures API Endpoint](https://api.jisuapi.com/futures)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and JISU_API_KEY; returns JSON-formatted futures data or structured error objects.]

## Skill Version(s):

1.0.8 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
