## Description:

Explore, filter, summarize, and visualize CSV data directly in terminal with interactive queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[derick001](https://clawhub.ai/user/derick001)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and engineers use this skill to inspect CSV files in a terminal, filter and select rows or columns, calculate basic statistics, create simple histograms, and export filtered results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The filter feature is flagged by the authoritative security evidence as capable of running unintended code if given a malicious condition.

Mitigation: Do not run filter conditions copied from untrusted sources; review conditions before execution and constrain or disable filtering in higher-risk environments.

Risk: The skill can export CSV or JSON files to user-supplied paths, and exported CSVs from untrusted input may be unsafe to open directly in spreadsheet software.

Mitigation: Use fresh output filenames in a controlled directory and sanitize exported CSVs before opening them in spreadsheet tools.

## Reference(s):

- [CSV Data Explorer README](artifact/README.md)
- [ClawHub skill page](https://clawhub.ai/derick001/skills/csv-data-explorer)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Files, Guidance]

**Output Format:** [Terminal text with optional CSV, JSON, or PNG output files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3; pandas is used for analysis, filtering, and export, and matplotlib is optional for enhanced charts.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
