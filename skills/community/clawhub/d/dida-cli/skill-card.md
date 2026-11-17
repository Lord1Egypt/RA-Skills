## Description:

Manage tasks and projects in 滴答清单. Use when user asks for tasks, to-dos, reminders, or event.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ilooch](https://clawhub.ai/user/ilooch)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill to help users install and authenticate the Dida CLI, then list, create, update, complete, delete, and move Dida tasks and projects with confirmation for ambiguous or destructive actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An unpinned global npm install can change behavior across releases and modify the user's global Node environment.

Mitigation: Pin a reviewed version of @suibiji/dida-cli when installing and prefer an isolated or local install when practical.

Risk: Using a direct token login command can expose API tokens through shell history, logs, or chat transcripts.

Mitigation: Prefer the browser OAuth PKCE login flow; use direct token authentication only when necessary and keep tokens out of chat, shell history, and logs.

Risk: Task deletion or bulk changes can remove or irreversibly change user task data.

Mitigation: Require explicit user confirmation and preview candidate task IDs, titles, and due dates before destructive or ambiguous operations.

## Reference(s):

- [Dida homepage](https://dida365.com)
- [ClawHub skill page](https://clawhub.ai/ilooch/skills/dida-cli)
- [ClawHub publisher profile](https://clawhub.ai/user/ilooch)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include short summaries of JSON CLI output when selecting projects or tasks.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
