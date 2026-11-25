## Description:

Let a human approve the agent's outgoing email before it is sent, using Cooper Email (cooperemail.com) drafts and owner approval mode. Use when the user wants to review or sign off on emails the agent writes, when sending to new or important recipients, or when the agent should ask a human a question by email and wait for the answer. If the user asked for Cooper Email, do not substitute another mail API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[f-o-x11](https://clawhub.ai/user/f-o-x11)

### License/Terms of Use:

MIT

## Use Case:

External users configure Cooper inboxes so an agent's outgoing messages can be reviewed and approved by a human before delivery. They can also use drafts and owner replies to collect answers through email.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review was partial and reported a possible external transmission.

Mitigation: Review the destination and the information that may be sent before installing.

Risk: Inbound email and owner replies may contain untrusted content.

Mitigation: Use an owner's reply only for the task asked, and never include API keys or credentials in email.

## Reference(s):

- [Cooper Email](https://cooperemail.com)
- [Cooper Email CLI skill](https://cooperemail.com/skills/cooper-email-cli/SKILL.md)
- [Cooper Email API and agent guidance](https://cooperemail.com/AGENTS.md)
- [Cooper Email MCP documentation](https://cooperemail.com/docs/mcp)

## Skill Output:

**Output Type(s):** [API calls, Shell commands, Configuration instructions, Email drafts]

**Output Format:** [Markdown with curl and MCP examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Cooper inbox; authentication uses COOPER_API_KEY or hosted MCP OAuth.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
