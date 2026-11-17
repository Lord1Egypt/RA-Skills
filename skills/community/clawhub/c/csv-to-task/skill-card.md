## Description:

Converts CSV rows into structured, trackable tasks such as Jira-style tickets, Markdown checklists, JSON arrays, or CSV rows with task fields.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangjipeng977](https://clawhub.ai/user/wangjipeng977)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and productivity-focused users use this skill to convert user-provided CSV or tabular backlog data into consistent task objects while preserving one task per input row.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-provided CSV content can contain sensitive, incomplete, or incorrect tabular data that may be carried into generated tasks.

Mitigation: Review the CSV content before use and confirm row counts, field mappings, assignees, priorities, and due dates before importing tasks into another system.

Risk: Packaging and documentation inconsistencies may create incorrect expectations about setup or test coverage.

Mitigation: Treat the included tests and contributor docs as rough packaging scaffolding and validate the skill behavior in the target agent environment before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangjipeng977/skills/csv-to-task)
- [Skill metadata source](https://github.com/MiniMax-AI/skills)
- [References index](references/index.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, CSV, Guidance]

**Output Format:** [Markdown checklists, Jira-style text, JSON arrays, or CSV with added task fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One output task per input row; original CSV data should be preserved as task metadata.]

## Skill Version(s):

1.0.1 (source: server release metadata and CHANGELOG.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
