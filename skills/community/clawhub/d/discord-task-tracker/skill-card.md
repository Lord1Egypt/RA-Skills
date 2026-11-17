## Description:

Track tasks in Discord using natural language. Add, list, complete, and delete tasks via chat commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fuzzyb33s](https://clawhub.ai/user/fuzzyb33s)

### License/Terms of Use:

MIT-0

## Use Case:

Discord users and workspace maintainers use this skill to maintain a lightweight task list from chat commands, including adding, listing, completing, and deleting tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A shared local task file can expose or mix tasks across Discord users or channels.

Mitigation: Use for personal or single-channel task lists unless per-user or per-channel task ownership is added.

Risk: Completion and deletion remove tasks from the active list, which can cause accidental data loss.

Mitigation: Make completion and deletion permanence clear before use and keep backups if task history matters.

Risk: Task text is echoed back into Discord-formatted responses.

Mitigation: Escape or sanitize Discord-formatted task text before using the skill in a multi-user Discord environment.

## Reference(s):

- [Command Reference](references/commands.md)
- [ClawHub Skill Page](https://clawhub.ai/fuzzyb33s/skills/discord-task-tracker)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration]

**Output Format:** [Discord-ready text and Markdown responses with optional command-line invocation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores task state in a local JSON file.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
