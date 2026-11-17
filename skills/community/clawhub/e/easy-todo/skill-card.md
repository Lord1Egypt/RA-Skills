## Description:

Personal TODO list manager. Add tasks with deadlines and priorities, mark them done, set up recurring items, and receive morning and evening summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[simenfur](https://clawhub.ai/user/simenfur)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to manage a local personal TODO list through an agent, including one-off tasks, recurring tasks, deadlines, priorities, and scheduled morning and evening summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic reminders and recurring task materialization can create or surface tasks without a direct user prompt.

Mitigation: Review scheduled summary behavior and recurring task settings before enabling automatic execution.

Risk: Important task data is stored in a local todos.md file and may be affected by fragile storage parsing.

Mitigation: Keep backups for important task data and avoid adding untrusted task text or reserved storage markers.

Risk: Changing TODOS_FILE can direct the skill to read or write an unintended local file.

Mitigation: Leave TODOS_FILE at its default or point it only to a dedicated TODO file.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/simenfur/skills/easy-todo)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Plain text CLI responses and Markdown task list updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and local todos.md storage.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
