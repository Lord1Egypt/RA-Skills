## Description:

Manages personal to-dos from natural-language requests, including creating, organizing, updating, and reviewing tasks through a command-line interface and optional local web UI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[awamwang](https://clawhub.ai/user/awamwang)

### License/Terms of Use:

MIT-0

## Use Case:

External users use the skill to capture and manage personal tasks, including dependencies, subtasks, deadlines, and task status, with optional local web access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private task details may be exposed, and important records may be affected.

Mitigation: Wait for fixes before using private or important records; for evaluation, use isolated test data and keep the web service off.

Risk: Files outside the storage folder may be overwritten.

Mitigation: Avoid batch-file editor commands and back up migration destinations.

Risk: The Windows launcher may stop unrelated services.

Mitigation: Avoid the Windows launcher pending fixes.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/awamwang/skills/awam-todo)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration]

**Output Format:** [English CLI/API text, JSON triage results, and persisted task records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Task data is stored locally; an optional local web UI can display and manage it.]

## Skill Version(s):

0.7.2 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
