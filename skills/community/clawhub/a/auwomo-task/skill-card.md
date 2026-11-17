## Description:

Auwomo Task helps agents manage Feishu task workflows by viewing task context, recording progress, creating main and subtask structures, and generating reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tyqqj0](https://clawhub.ai/user/tyqqj0)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and managers using Auwomo with Feishu tasks use this skill to inspect personal or team task context, record completed work into task trees, create long-running work streams, and draft daily or weekly progress reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access Feishu task data, team or subordinate task context, and Cotrace work-history summaries.

Mitigation: Install it only for agents and users that are expected to handle that work data, and verify identity and authorization before task operations.

Risk: Broad triggers and automated flows may treat vague work updates as requests to create persistent task records.

Mitigation: Use explicit wording and require confirmation for ambiguous updates, sensitive content, or cron-driven recording.

Risk: The skill can write persistent task records and create task structures through the Auwomo CLI.

Mitigation: Review the selected parent task, summary, and description before executing write or create commands, especially when the match is uncertain.

## Reference(s):

- [Task Context](references/task-context.md)
- [Task Record](references/task-record.md)
- [Task Create](references/task-create.md)
- [Task Report](references/task-report.md)
- [Task Check](references/task-check.md)
- [Cron Templates](references/cron-templates.md)
- [ClawHub Skill Page](https://clawhub.ai/tyqqj0/skills/auwomo-task)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and human-readable task summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include JSON-oriented CLI options for machine-readable Feishu task context and checks.]

## Skill Version(s):

1.5.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
