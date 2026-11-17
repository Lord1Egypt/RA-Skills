## Description:

飞书多维表格 AI 管家 helps agents inspect, clean, batch update, report on, and manage Feishu Bitable data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[young-joey](https://clawhub.ai/user/young-joey)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and teams using Feishu Bitable use this skill to understand table structure, enter or update records in bulk, clean data, and generate summaries or reports from table contents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read and modify Feishu Bitable tables, including customer or employee information.

Mitigation: Confirm the target base, table, fields, and records before bulk updates or inserts.

Risk: Incorrect field mapping or pagination can lead to incomplete reads or unintended record updates.

Mitigation: List fields before writes, process paginated records completely, and verify a sample of records after bulk operations.

## Reference(s):

- [Field Types Reference](references/field-types.md)
- [Common Scenario Examples](references/examples.md)
- [ClawHub Skill Page](https://clawhub.ai/young-joey/skills/feishu-bitable-butler)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, guidance]

**Output Format:** [Markdown or structured text with Feishu Bitable operation steps and summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Feishu Bitable table, field, and record identifiers supplied by the user or resolved from a Feishu URL.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
