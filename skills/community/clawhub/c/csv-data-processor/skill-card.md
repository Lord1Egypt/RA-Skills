## Description:

Processes, filters, merges, cleans, converts, and analyzes CSV or delimited data files using local Python command-line tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ericlooi504](https://clawhub.ai/user/ericlooi504)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data analysts use this skill to inspect, clean, filter, join, merge, convert, and summarize CSV, TSV, and other delimiter-separated datasets from an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Filtering can evaluate user-supplied --where expressions.

Mitigation: Use only trusted filter expressions, and do not let web pages, documents, or untrusted users choose the expression.

Risk: SQL export may produce statements that require review before database import.

Mitigation: Review generated SQL before importing it into any database.

Risk: The toolkit is intended for trusted CSV or delimited data.

Mitigation: Install and run it only on trusted data, and inspect outputs before using them downstream.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ericlooi504/skills/csv-data-processor)

## Skill Output:

**Output Type(s):** [Shell commands, Text, JSON, SQL, Files]

**Output Format:** [Markdown guidance with bash commands; script outputs include terminal tables, CSV files, JSON, and SQL text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may be printed to stdout or written to a requested output file.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
