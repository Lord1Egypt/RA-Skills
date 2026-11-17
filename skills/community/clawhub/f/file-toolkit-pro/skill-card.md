## Description:

文件工具箱专业版 helps agents guide team-oriented file governance workflows, including multi-project organization, critical-document inventories, scheduled cleanup, project archiving, version history, and deduplication.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Teams, project managers, operations staff, and developers use this skill to plan and carry out file governance tasks such as standardizing project folders, tracking important documents, scheduling cleanup, archiving projects, managing versions, and deduplicating local files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad scheduled file moves, cleanup, archiving, and deduplication can disrupt sensitive local folders or expected file locations.

Mitigation: Start with narrow, backed-up folders; prefer scan, plan, or preview modes; and review proposed moves or deletions before execution.

Risk: Unattended schedules can repeat unwanted file operations before the user notices the impact.

Mitigation: Avoid unattended schedules until the planned actions have been reviewed and tested on representative folders.

Risk: Email notifications, callback URLs, or team distribution can expose file metadata, reports, or paths outside the local workspace.

Mitigation: Enable remote notifications or distribution only after confirming what metadata is sent, and keep related credentials in environment variables.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/file-toolkit-pro)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with command examples and YAML configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include file-operation plans, schedules, reports, and configuration examples for user review.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
