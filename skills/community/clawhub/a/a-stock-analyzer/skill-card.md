## Description:

A Stock Analyzer analyzes China A-share market indices and screens stocks using technical and financial criteria to produce markdown trading reports with buy ranges, targets, stop-loss levels, and position sizing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dxihyv](https://clawhub.ai/user/dxihyv)

### License/Terms of Use:

MIT-0

## Use Case:

External investors and market-analysis users can use this skill to generate China A-share market summaries, stock screens, and markdown reports with suggested buy ranges, targets, stop-loss levels, and position allocations. Users should review the generated analysis before acting on it.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated reports can contain actionable trading recommendations based on inconsistent or substituted financial data.

Mitigation: Review every report and verify market and financial inputs independently before making investment decisions.

Risk: Optional webhook push delivery can send report content to a configured messaging service.

Mitigation: Leave push webhooks unconfigured or disabled unless outbound report sharing is intended and approved.

Risk: Unpinned dependencies can change behavior over time.

Mitigation: Run the skill in a pinned dependency environment and review dependency versions before deployment.

## Reference(s):

- [A Stock Analyzer on ClawHub](https://clawhub.ai/dxihyv/skills/a-stock-analyzer)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports and terminal text with optional shell commands and JSON configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports may include stock recommendations, buy ranges, target prices, stop-loss levels, risk notes, and optional webhook push summaries.]

## Skill Version(s):

2.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
