## Description:

Provides an execution framework for aggressive growth stock screening, individual stock analysis, market season assessment, and position planning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenxyzcyxpp](https://clawhub.ai/user/chenxyzcyxpp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to screen A-share small-cap growth candidates, generate structured stock analysis reports, judge market-cycle posture, and draft staged entry or exit plans. It should be treated as research support rather than personalized financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can produce actionable trading, position sizing, buy, and sell guidance from incomplete or unverified financial data.

Mitigation: Use it only as a research aid, verify all figures independently, and avoid following its trade or position guidance when any data source fails or financial verification is incomplete.

Risk: The scripts depend on live market-data sources and Python packages that may fail, change behavior, or return inconsistent values.

Mitigation: Install dependencies in an isolated environment with pinned, reviewed package versions, and require reports to label failed or unverified data rather than filling missing values.

## Reference(s):

- [Screening criteria](references/screening_criteria.md)
- [Stock analysis report template](templates/stock_analysis_report.md)
- [ClawHub skill page](https://clawhub.ai/chenxyzcyxpp/skills/aggressive-growth-strategy)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown reports, JSON screening results, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include market-data source labels, failed-data markers, financial verification status, scores, ratings, and position guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
