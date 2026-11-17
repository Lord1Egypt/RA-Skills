## Description:

ENI收割者v14 analyzes public A-share limit-up stock data through AkShare and returns a markdown table of stocks with at least two consecutive limit-up days plus turnover entropy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gxfc888aa](https://clawhub.ai/user/gxfc888aa)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and market-analysis agents use this skill to fetch public A-share limit-up pool data, filter for stocks with at least two consecutive limit-up days, and review the resulting names, industries, and turnover-entropy values.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes outbound requests through AkShare to retrieve live public market data.

Mitigation: Run it in a least-privileged environment with network access limited to expected market-data sources.

Risk: The artifact declares unpinned akshare and pandas dependencies.

Mitigation: Pin dependency versions before production use and review updates before installing them.

Risk: The skill returns market-analysis output that may be delayed, unavailable, or unsuitable as trading advice.

Mitigation: Treat results as informational screening data and verify them against authoritative market sources before acting.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gxfc888aa/skills/eni-predator-01)
- [Publisher profile](https://clawhub.ai/user/gxfc888aa)

## Skill Output:

**Output Type(s):** [text, markdown]

**Output Format:** [Markdown table or short plain-text status/error message]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May pause briefly before returning results and depends on current public AkShare market-data availability.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
