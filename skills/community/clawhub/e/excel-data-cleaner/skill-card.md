## Description:

Profiles and cleans user-provided Excel or CSV data, then helps produce statistics, a cleaning report, and practical conclusions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[petehuax](https://clawhub.ai/user/petehuax)

### License/Terms of Use:

MIT-0

## Use Case:

People working with raw spreadsheets or CSV files use this skill to inspect missing values, duplicates, and outliers, clean data using a chosen strategy, and summarize results with actionable conclusions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Removing duplicates or rows, clipping outliers, and filling missing values may change data needed for analysis.

Mitigation: Review the profile and agree on a cleaning strategy first; inspect the cleaning log and compare the result with the original.

Risk: Choosing an existing output or report path may overwrite a file.

Mitigation: Choose new output paths deliberately and keep backups of the original data.

## Reference(s):

- [Excel Data Cleaner on ClawHub](https://clawhub.ai/petehuax/skills/excel-data-cleaner)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Guidance]

**Output Format:** [Console profile and cleaning log; cleaned XLSX or CSV file; optional Markdown report and agent-written analysis]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The output file and optional report paths are configurable; cleaning actions are recorded for review.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
