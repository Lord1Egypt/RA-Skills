## Description:

Interactive CSV data-cleaning CLI support for type inference, missing-value handling, duplicate detection, column-name standardization, and CSV export.

This skill is ready for commercial/non-commercial use.

## Publisher:

[antonia-sz](https://clawhub.ai/user/antonia-sz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, data analysts, and operations teams use this skill to inspect CSV files, preview dataset shape, clean missing values, remove duplicates, standardize columns, and export cleaned CSV files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CSV-cleaning options can change datasets by dropping rows, filling missing values, deduplicating records, or standardizing column names.

Mitigation: Run the skill on copies of important CSV files and review previews, summaries, and output diffs before using cleaned data downstream.

Risk: The inspected artifact declares a CLI entrypoint but does not include the referenced executable.

Mitigation: Confirm that the installer supplies the executable or provide an equivalent implementation before relying on the skill operationally.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/antonia-sz/skills/csv-wizard)
- [ClawHub publisher profile](https://clawhub.ai/user/antonia-sz)

## Skill Output:

**Output Type(s):** [Shell commands, Files, Analysis, Guidance]

**Output Format:** [Markdown with inline shell commands and CSV file outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May modify tabular data by dropping rows, filling missing values, deduplicating records, standardizing names, and exporting cleaned CSV files.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter: 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
