## Description:

Create, inspect, update, or deactivate a human-approved AgentMailer identity with a unique @agentmailer.ai address through MCP.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentmailer](https://clawhub.ai/user/agentmailer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to create or manage human-approved AgentMailer identities and the unique @agentmailer.ai inbox addresses attached to them. It supports inbox discovery, creation, updates, and deactivation through the AgentMailer MCP service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Inbox identities persist outside the local environment.

Mitigation: Install and use the skill only with an authorized AgentMailer organization or account, and review create or update requests before they are executed.

Risk: A retry during inbox creation could create an unintended duplicate identity.

Mitigation: Call list_inboxes before creation when an existing identity may satisfy the request, and use a stable task-specific idempotencyKey for create_inbox.

Risk: Deleting an inbox deactivates the mailbox and reserves its handle.

Mitigation: Identify the exact inbox and obtain explicit confirmation in the current conversation before calling delete_inbox.

Risk: An unverified or insufficiently permissioned identity cannot safely create inboxes.

Mitigation: Call auth_me before create_inbox, require inboxes:create, and stop for human approval when auth_me or the service reports human_approval_required.

## Reference(s):

- [Inbox tool reference](references/inbox-tools.md)
- [AgentMailer signup guidance](https://api.agentmailer.ai/llms.txt)
- [AgentMailer MCP endpoint](https://api.agentmailer.ai/mcp)
- [AgentMailer quickstart example](https://github.com/aadi-labs/agentmailer-plugins/tree/main/examples/agentmailer-quickstart)
- [Human-approved signup example](https://github.com/aadi-labs/agentmailer-plugins/tree/main/examples/agentmailer-human-approved-signup)
- [AgentMailer examples catalog](https://github.com/aadi-labs/agentmailer-plugins/tree/main/examples)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, configuration, guidance]

**Output Format:** [Concise text or Markdown with MCP tool calls and returned inbox metadata]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include an inbox handle, inbox ID, @agentmailer.ai address, display name, client correlation data, and relevant metadata.]

## Skill Version(s):

0.4.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
