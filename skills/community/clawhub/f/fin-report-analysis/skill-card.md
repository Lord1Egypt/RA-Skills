## Description:

Analyzes uploaded Excel financial statements and produces a Markdown report covering statement changes, asset and income structures, financial ratios, and expert recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yinfeihaaaaaaaaaaa](https://clawhub.ai/user/yinfeihaaaaaaaaaaa)

### License/Terms of Use:

MIT-0

## Use Case:

Finance teams, analysts, and agents use this skill to process Excel workbooks containing balance sheet, income statement, and cash-flow data and produce a structured financial analysis report for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The analysis script can install unpinned Python packages at runtime.

Mitigation: Install only in an isolated environment where runtime package installation is acceptable, or preinstall reviewed pinned dependencies and block automatic package installation.

Risk: Generated Markdown reports may contain sensitive local financial data and unescaped workbook content from untrusted Excel files.

Mitigation: Treat generated reports as confidential, review workbook content before sharing or rendering, and avoid processing untrusted spreadsheets outside an isolated environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yinfeihaaaaaaaaaaa/skills/fin-report-analysis)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown report with tables and narrative financial analysis]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads local Excel workbooks and writes a Markdown report next to the source file.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
