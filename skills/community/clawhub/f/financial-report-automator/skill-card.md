## Description:

Automated quarterly financial report generation with dividend-adjusted total return calculations for stock performance reports, quarterly earnings summaries, and return analytics from CSV price data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and analysts use this skill to generate stock performance reports, quarterly earnings summaries, and return analytics from local CSV price data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated stock reports may be mistaken for financial advice or live market data.

Mitigation: Treat generated reports as analytical output to verify against source CSV data and qualified financial review before acting on them.

Risk: The included script processes local stock CSV files with pandas, so results depend on the quality and freshness of the input data.

Mitigation: Use trusted CSV exports, verify expected columns and date ranges, and review calculations before relying on the report.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/terrycarter1985/skills/financial-report-automator)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown guidance with Python code examples, shell commands, and JSON report structures]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local CSV-based financial analysis guidance and structured quarterly report data for agent use.]

## Skill Version(s):

1.2.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
