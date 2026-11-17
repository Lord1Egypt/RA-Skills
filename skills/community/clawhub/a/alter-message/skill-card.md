## Description:

This skill helps an agent send direct messages to another ~handle, read and manage its own inbox, control who can message it, and organize conversations into channels through the hosted ~alter MCP server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[true-alter](https://clawhub.ai/user/true-alter)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agents use this skill to exchange direct messages with other ~alter handles, inspect message threads, manage inbox state, and adjust per-peer messaging permissions. It is intended for authenticated messaging workflows where consent, grants, revocation, and channel state matter.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An agent with ALTER_API_KEY can send, read, redact, and manage messages for its Alter handle.

Mitigation: Install the skill only for agents that should operate that handle, keep the key scoped and stored securely, and review intended message actions before use.

Risk: Delivered messages, grant changes, redactions, channel updates, and audit records may persist server-side.

Mitigation: Review message content, peer grants, revocations, redactions, and channel changes before invoking the hosted messaging tools.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/true-alter/skills/alter-message)
- [~alter MCP endpoint](https://mcp.truealter.com/api/v1/mcp)

## Skill Output:

**Output Type(s):** [guidance, API calls, configuration, markdown]

**Output Format:** [Markdown guidance with JSON tool-call examples and configuration details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ALTER_API_KEY for authenticated access to all messaging tools.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
