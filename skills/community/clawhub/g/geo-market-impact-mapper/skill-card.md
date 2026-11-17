## Description:

Gets and analyzes crude oil and gold futures price movement, detects market-move thresholds, and maps commodity changes to geopolitical event impact paths.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liweijie0709-cmyk](https://clawhub.ai/user/liweijie0709-cmyk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to fetch public crude oil and gold futures prices, compute percentage movement, and summarize possible sector impacts for geopolitical or market events. The output is informational market-impact analysis, not financial advice or an automated trading signal.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill performs outbound Yahoo Finance price lookups, which may be unsuitable in restricted environments or fail when public market-data access is unavailable.

Mitigation: Install only where outbound public commodity price requests fit the environment, and handle unavailable market data as an expected operational condition.

Risk: Generated sector impacts and event scoring could be mistaken for investment advice or an automated trading signal.

Mitigation: Use the outputs as informational market-impact analysis and require human review before any trading, portfolio, or risk decision.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liweijie0709-cmyk/skills/geo-market-impact-mapper)
- [Artifact skill documentation](artifact/SKILL.md)
- [Artifact Python module](artifact/geo_market_impact_mapper.py)

## Skill Output:

**Output Type(s):** [Text, Code, Analysis]

**Output Format:** [Python module outputs, dictionaries, and Chinese-language text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Fetches public Yahoo Finance commodity price data for WTI crude oil and gold futures when network access is available.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
