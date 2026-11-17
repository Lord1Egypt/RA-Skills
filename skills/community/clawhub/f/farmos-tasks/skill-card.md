## Description:

Query and manage farm work orders and tasks, including assignments, task creation, status updates, and restock follow-ups.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brianppetty](https://clawhub.ai/user/brianppetty)

### License/Terms of Use:


## Use Case:

Farm managers and farm operations staff use this skill to inspect task and work-order status, create or assign tasks with confirmation, and track field, equipment, and procurement follow-ups.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles operational task data through insecure or under-protected API patterns.

Mitigation: Use it only on a trusted, isolated FarmOS network, require authentication for task reads when possible, and use HTTPS for any request carrying tokens or task details.

Risk: Authenticated endpoints can create, assign, or change farm tasks.

Mitigation: Require explicit confirmation before writes and use the JWT role that matches the requesting user's permissions.

Risk: Natural-language task detection may treat casual comments as actionable work.

Mitigation: Confirm task title, priority, assignee, and due date before creating or updating tasks.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/brianppetty/skills/farmos-tasks)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance, API calls]

**Output Format:** [Markdown with inline JSON and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include task summaries, confirmation prompts, and FarmOS API request details.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
