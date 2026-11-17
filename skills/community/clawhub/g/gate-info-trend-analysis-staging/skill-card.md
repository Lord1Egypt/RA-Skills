## Description:

Provides read-only single-coin crypto trend and technical analysis using Gate market snapshots, K-line data, indicator history, and multi-timeframe technical signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gaixianggeng](https://clawhub.ai/user/gaixianggeng)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to produce focused technical-analysis reports for one crypto asset when the request is limited to trend, indicator, K-line, support, or resistance analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan reports that the skill delegates mandatory runtime authority to parent-directory rule files that are not part of the reviewed artifact.

Mitigation: Install only in environments where the parent runtime-rule files are trusted and controlled, and review changes to those files as behavior-changing updates.

Risk: Technical analysis can be misleading when source market data, indicators, or timeframes are incomplete or unavailable.

Mitigation: Label timeframe and indicator settings, disclose unavailable data, downgrade confidence when signals conflict or data is missing, and avoid trading or price-prediction advice.

## Reference(s):

- [MCP execution specification](references/mcp.md)
- [Scenarios and prompt examples](references/scenarios.md)
- [ClawHub skill page](https://clawhub.ai/gaixianggeng/skills/gate-info-trend-analysis-staging)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown technical analysis report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes current snapshot, trend assessment, indicator details, support and resistance levels, multi-timeframe signal summary, overall assessment, and risk warnings.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
