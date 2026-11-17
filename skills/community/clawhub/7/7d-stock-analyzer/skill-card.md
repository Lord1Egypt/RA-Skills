## Description:

7d Stock Analyzer provides a seven-dimension stock analysis workflow that combines efinance, AKShare, and QVeris sources to produce stock-analysis reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xuanpass](https://clawhub.ai/user/xuanpass)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to run stock analysis across data collection, fundamentals, valuation, industry position, technical indicators, risk, and conclusion reporting. The generated reports are decision-support artifacts and should not be treated as investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated stock scores and investment conclusions may appear data-derived even when placeholder or default logic contributed to them.

Mitigation: Treat reports as experimental scaffolding, manually verify all scores and conclusions, and do not use the output for real trading decisions.

Risk: The skill depends on third-party Python packages and market data sources that may be unavailable, delayed, incomplete, or changed upstream.

Mitigation: Install dependencies in an isolated environment with reviewed and pinned versions, and confirm source data quality before relying on any report.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xuanpass/skills/7d-stock-analyzer)
- [Artifact README](artifact/README.md)
- [Skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, guidance]

**Output Format:** [Markdown reports, JSON reports, brief text summaries, and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3; optional QVERIS_API_KEY enables the QVeris adapter when implemented.]

## Skill Version(s):

1.0.2 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
