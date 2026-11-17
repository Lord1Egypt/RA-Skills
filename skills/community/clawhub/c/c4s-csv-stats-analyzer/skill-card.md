## Description:

Analyzes any CSV file and returns row count, column names, and basic statistics for numeric columns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[democ4s](https://clawhub.ai/user/democ4s)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and other external users can invoke this skill to quickly inspect a readable CSV file and summarize its shape and numeric columns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs through uv and may download pandas at runtime because the dependency is not pinned in the artifact.

Mitigation: Install only where runtime dependency downloads are acceptable, or run in a constrained environment with reviewed dependencies.

Risk: Untrusted CSV content or crafted headers may affect terminal display or confuse interpretation of the reported output.

Mitigation: Use trusted CSV files when possible, and inspect output carefully or run the skill in a constrained environment for untrusted files.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/democ4s/skills/c4s-csv-stats-analyzer)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands]

**Output Format:** [Markdown text with CSV row count, column names, and numeric min, max, and average statistics.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads a user-specified CSV file and reports statistics without modifying the source file.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
