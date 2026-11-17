## Description:

Manage ClickUp tasks, lists, spaces, folders, comments, goals, and workspace data via the ClickUp API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hith3sh](https://clawhub.ai/user/hith3sh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, project managers, and ClickUp workspace users use this skill to manage project workflows, tasks, lists, spaces, folders, comments, goals, and workspace data from chat through a connected ClickUp account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Connected ClickUp workspace data may be created, updated, deleted, commented on, or messaged if the user approves a write action.

Mitigation: Review previews carefully and confirm the target resource, intended effect, and message or comment content before executing write actions.

Risk: Access follows the connected ClickUp account's workspace permissions, so broad account permissions increase the potential impact of mistakes.

Mitigation: Install only when the user trusts ClawLink and connect a ClickUp account with permissions appropriate for the intended workflow.

Risk: Bulk operations can affect multiple ClickUp records at once.

Mitigation: Confirm the scope and affected records before approving any bulk action.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/hith3sh/skills/clickup-tasks)
- [Publisher Profile](https://clawhub.ai/user/hith3sh)
- [ClickUp API Documentation](https://clickup.com/api)
- [ClickUp API Reference](https://clickup.com/api/docs)
- [ClawLink Docs](https://docs.claw-link.dev/openclaw)
- [ClawLink Verification](https://claw-link.dev/verify)
- [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=clickup-tasks)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash command examples and JSON parameter snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read operations can be performed directly; create, update, delete, bulk, comment, and chat-message actions require preview and explicit user confirmation.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
