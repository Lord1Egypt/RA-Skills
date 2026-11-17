## Description:

Manage family todo lists with multi-user support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thurendous](https://clawhub.ai/user/thurendous)

### License/Terms of Use:

MIT

## Use Case:

Family members and household automation agents use this skill to add, list, complete, delete, and review shared or per-person todo tasks from a local Node.js command line workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Any invoker in a shared chat or automation context can view, add, complete, or delete tasks across users.

Mitigation: Run the skill only for a single trusted user or behind an outer authentication and authorization layer that enforces task access by caller.

Risk: Todo contents are stored as plaintext local JSON.

Mitigation: Keep the working directory private, restrict filesystem permissions, and avoid storing sensitive household or personal information in tasks.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thurendous/skills/family-todo-management)
- [Publisher profile](https://clawhub.ai/user/thurendous)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration]

**Output Format:** [Markdown-formatted CLI text with configuration and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes todo data to local plaintext JSON storage under memory/todo.json.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
