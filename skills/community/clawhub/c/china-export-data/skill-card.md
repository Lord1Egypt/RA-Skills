## Description:

Query China's official export statistics with analyst-grade metrics across product dashboards, monthly trends, destination-market structure, fastest-growing markets, unit-price bands, industry-chain structure, and product opportunity rankings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[findhappy7](https://clawhub.ai/user/findhappy7)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and trade-research agents use this skill to look up China export statistics by HS code, compare destinations and growth signals, examine RMB-denominated unit-price bands, and identify product opportunities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts doumaotong.com to retrieve China export statistics.

Mitigation: Install only in environments where outbound access to DouMaoTong is expected and acceptable.

Risk: Export metrics may be misread as complete real-time trade or financial advice.

Mitigation: Use the skill for HS-code and China export-market analysis, state the covered period and source, and avoid treating outputs as general-purpose trade or financial advice.

Risk: Some endpoints return ranked subsets rather than full rankings.

Mitigation: Disclose Top N limits when presenting results and direct users to the full DouMaoTong report when they need broader coverage.

## Reference(s):

- [DouMaoTong](https://doumaotong.com)
- [ClawHub skill page](https://clawhub.ai/findhappy7/skills/china-export-data)
- [Publisher profile](https://clawhub.ai/user/findhappy7)

## Skill Output:

**Output Type(s):** [Text, Markdown, API Calls, Guidance]

**Output Format:** [Markdown responses with source attribution and optional JSON-derived tables or summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses should state the data source, RMB currency basis, relevant period, and any Top N subset limits.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
