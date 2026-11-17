## Description:

Helps agents inspect local CSV files, select columns, filter or deduplicate rows, and count records using Python's standard library.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other users can preview and filter local CSV data or count rows without installing third-party packages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Permission metadata says no filesystem access, but the tool reads local CSV files.

Mitigation: Approve local file access explicitly and review the documentation before use in strict approval workflows.

Risk: CSV contents may be printed to the agent or terminal, exposing sensitive records.

Mitigation: Avoid sensitive CSVs unless their contents are safe to display; limit previews when appropriate.

## Reference(s):

- [csv-slice on ClawHub](https://clawhub.ai/zhaoxinghua09-cell/skills/csv-slice)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [Plain-text table or count; optional JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include CSV contents, headers, row counts, and deduplication counts.]

## Skill Version(s):

1.0.6 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
