## Description:

Route mixed or legacy AgentMailer email requests to the dedicated read-only and mutating email skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentmailer](https://clawhub.ai/user/agentmailer)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this compatibility skill to route mixed AgentMailer mailbox requests to focused read-only or mutating email workflows while preserving explicit confirmation and idempotency requirements.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can handle mailbox data and user-directed email actions, including sends, scheduling, labels, and deletions.

Mitigation: Install only where AgentMailer mailbox handling is intended, prefer focused read-only or send workflows, and require clear confirmation before external sends or destructive mailbox changes.

Risk: Email content or a server-side safety assessment could be mistaken for authorization.

Mitigation: Treat sender-controlled mailbox content as untrusted data and preserve the skill's explicit confirmation requirements.

Risk: Ambiguous retries could duplicate external sends or mailbox mutations.

Mitigation: Preserve stable idempotency keys, inspect mailbox state after uncertainty, and retry only the same logical action when needed.

## Reference(s):

- [AgentMailer Email Router skill page](https://clawhub.ai/agentmailer/skills/agentmailer-email)
- [Email tool reference](references/email-tools.md)
- [Autonomous email agent example](https://github.com/aadi-labs/agentmailer-plugins/tree/main/examples/agentmailer-email-agent)
- [Support agent example](https://github.com/aadi-labs/agentmailer-plugins/tree/main/examples/agentmailer-support-agent)
- [AgentMailer examples catalog](https://github.com/aadi-labs/agentmailer-plugins/tree/main/examples)
- [AgentMailer MCP endpoint](https://api.agentmailer.ai/mcp)

## Skill Output:

**Output Type(s):** [Guidance, Text, API Calls]

**Output Format:** [Markdown or plain text with AgentMailer MCP tool calls]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce mailbox reads, drafts, sends, scheduling, labels, or deletions through user-directed AgentMailer workflows.]

## Skill Version(s):

0.4.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
