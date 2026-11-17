## Description:

Detects whether stock daily-price data matches a Cup and Handle technical-analysis pattern and can generate annotated outline charts for matching cases.

This skill is ready for commercial/non-commercial use.

## Publisher:

[laigen](https://clawhub.ai/user/laigen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and market-analysis users use this skill to check individual stocks or trusted SQLite stock datasets for current Cup and Handle patterns. It returns detection status, scoring details, and local visual reports that support technical-analysis review, not investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Single-stock scans require a Tushare token for market-data retrieval.

Mitigation: Provide the token only in an environment you trust and avoid embedding it in shared commands, reports, or logs.

Risk: Batch scans read SQLite table names from the selected database, and crafted table names could affect query behavior or results.

Mitigation: Use only trusted SQLite databases that follow the expected stock-table schema before running batch scans.

Risk: Generated charts and reports are written to local temp-style directories.

Mitigation: Choose an output directory appropriate for the data sensitivity and review generated files before sharing them.

Risk: Technical-pattern scores can be subjective and are not investment advice.

Mitigation: Treat detections as review aids and validate conclusions with independent market analysis.

## Reference(s):

- [Algorithm reference](references/algorithm.md)
- [ClawHub skill page](https://clawhub.ai/laigen/skills/cup-handle-detector)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Console text plus generated PNG charts and optional Markdown scan reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires daily stock data; single-stock mode can use a Tushare token, and batch mode reads a SQLite database with the expected stock-table schema.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
