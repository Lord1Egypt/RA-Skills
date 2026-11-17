## Description:

Feishu Bitable Merger merges data from multiple Feishu bitables into one target table.

This skill is ready for commercial/non-commercial use.

## Publisher:

[night556](https://clawhub.ai/user/night556)

### License/Terms of Use:

MIT

## Use Case:

Developers and operations teams use this skill to consolidate records from multiple Feishu Bitable tables into a prepared target table, including optional field mapping and duplicate removal.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill writes persistent records to the selected Feishu Bitable target table, so an incorrect target URL or field setup can affect production data.

Mitigation: Test on a copy or non-production table first, confirm source and target URLs, verify field compatibility, and keep a backup before running the merge.

Risk: The skill requires Feishu Bitable read and write permissions for apps and records.

Mitigation: Install only when those permissions are acceptable for the workspace and use credentials with the minimum access needed for the merge.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/night556/skills/feishu-bitable-merger)
- [Publisher profile](https://clawhub.ai/user/night556)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs a merge workflow that reads Feishu Bitable records and writes persistent records to the target table.]

## Skill Version(s):

1.0.0 (source: package.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
