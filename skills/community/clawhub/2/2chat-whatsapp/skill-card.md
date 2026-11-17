## Description:

Connects an OpenClaw agent to 2Chat so it can send and read WhatsApp and SMS messages, manage WhatsApp Business templates, contacts, channels, groups, statuses, catalogs, and call records.

This skill is ready for commercial/non-commercial use.

## Publisher:

[2chat](https://clawhub.ai/user/2chat)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and operations teams use this skill to let an agent work with a connected 2Chat account for WhatsApp, SMS, contact, channel, catalog, status, and call-record workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent can send WhatsApp or SMS messages, publish statuses, run channel commands, and take other actions that affect real accounts or may cost money.

Mitigation: Review recipients, message bodies, selected channels, and paid actions before approving tool calls.

Risk: Contact deletion and similar account-management actions can be permanent.

Mitigation: Confirm the exact contact UUID and intended action before approving destructive changes.

Risk: Using the skill gives 2Chat access to the WhatsApp, SMS, contact, and call-record data involved in the workflow.

Mitigation: Install and connect the skill only when 2Chat is trusted for the relevant account data.

## Reference(s):

- [ClawHub listing: WhatsApp & Calls](https://clawhub.ai/2chat/skills/2chat-whatsapp)
- [2Chat homepage](https://2chat.co)
- [2Chat MCP setup documentation](https://developers.2chat.co/docs/MCP/setup)
- [2Chat MCP endpoint](https://mcp.2chat.io/mcp)

## Skill Output:

**Output Type(s):** [Text, API Calls, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON configuration, and remote MCP tool calls]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires OpenClaw, a 2Chat account, OAuth browser sign-in, and access to mcp.2chat.io.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
