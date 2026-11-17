## Description:

Cn Todo Today provides a lightweight Chinese-language command-line todo manager implemented with the Python standard library.

This skill is ready for commercial/non-commercial use.

## Publisher:

[freedompixels](https://clawhub.ai/user/freedompixels)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to add, list, complete, delete, and summarize same-day todo items through a local Python command-line helper.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Todo text is stored locally in ~/.cn_todo_today.json and may contain sensitive user-entered information.

Mitigation: Avoid storing secrets or regulated data in todo items and protect the local user account and home directory.

Risk: Deleting todo items removes them from the active local todo list, and the evidence notes data-retention caveats.

Mitigation: Back up ~/.cn_todo_today.json before cleanup or deletion when retention matters.

## Reference(s):

- [Cn Todo Today on ClawHub](https://clawhub.ai/freedompixels/skills/cn-todo-today)
- [Publisher profile: freedompixels](https://clawhub.ai/user/freedompixels)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell command examples and plain-text command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Todo data is stored locally in ~/.cn_todo_today.json.]

## Skill Version(s):

1.2.6 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
