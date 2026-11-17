## Description:

Manage Apple Reminders via remindctl CLI (list, add, edit, complete, delete). Supports lists, date filters, and JSON/plain output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huangfeng1995](https://clawhub.ai/user/huangfeng1995)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to have an agent manage Apple Reminders through the remindctl command-line tool, including listing, creating, completing, and deleting reminders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill documents reminder and list deletion commands that can remove user data.

Mitigation: Review delete and list-delete actions before approving execution, especially commands using force flags.

Risk: The skill manages personal Apple Reminders through an external CLI on macOS.

Mitigation: Install only when the agent should manage Apple Reminders, and grant Reminders permission only for that intended use.

## Reference(s):

- [Apple Reminders.Old on ClawHub](https://clawhub.ai/huangfeng1995/skills/apple-reminders-old)
- [remindctl GitHub repository](https://github.com/steipete/remindctl)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash command examples and plain-text guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can reference JSON, TSV/plain, and quiet output modes supported by remindctl.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
