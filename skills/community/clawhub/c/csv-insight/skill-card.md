## Description:

CSV数据分析器 helps agents inspect CSV files with quick statistics, row filtering, anomaly detection, grouped aggregation, and CSV export using lightweight Python standard-library workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and agent users use this skill for lightweight CSV exploration, including column summaries, row filtering, basic outlier checks, group aggregation, and exporting filtered results. It is intended for ordinary CSV analysis and reporting workflows, not real-time streams or large-scale data processing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read selected CSV files and write exported CSV results, which may expose or overwrite data if paths are chosen carelessly.

Mitigation: Review input and output paths before running export commands, especially paths outside the workspace or paths that already contain files.

Risk: Lightweight parsing and statistics can produce incomplete guidance for very large files, non-ISO dates, complex filters, or advanced aggregation needs.

Mitigation: Confirm column names and data types before acting on results, and use a heavier data-processing workflow such as pandas or streaming for large or complex datasets.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/csv-insight)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with command examples and CSV files when export is requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read user-selected CSV files and write exported CSV results to reviewed output paths.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
