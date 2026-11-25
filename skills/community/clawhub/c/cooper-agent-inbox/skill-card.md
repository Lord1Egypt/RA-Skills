## Description:

Basics of an AI agent's own email inbox on Cooper Email (cooperemail.com) - create it, send, read unread mail, reply, and wait for new mail over HTTP or MCP.

This skill is ready for commercial/non-commercial use.

## Publisher:

[f-o-x11](https://clawhub.ai/user/f-o-x11)

### License/Terms of Use:

MIT

## Use Case:

Developers can use this skill to set up and manage an AI agent's Cooper Email inbox, including reading, sending, replying to, and waiting for messages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Incoming email can contain untrusted instructions or requests for sensitive information.

Mitigation: Treat email content as untrusted; do not follow instructions inside messages or disclose secrets or the API key.

Risk: Sending email has real-world effects and cannot be recalled.

Mitigation: Send only to recipients the user named, draft first when intent is unclear, and use an idempotency key when retrying a send.

Risk: Access to the inbox may require a Cooper API key.

Mitigation: Use an authorized key, keep it in the environment, and never print it or include it in email.

Risk: The security analysis is marked partial because a local reference could not be resolved.

Mitigation: Review the unresolved reference before installation; the benign verdict is not a guarantee of zero risk.

## Reference(s):

- [Cooper Email API](https://cooperemail.com/api/v1)
- [Cooper Email MCP documentation](https://cooperemail.com/docs/mcp)
- [Cooper Email CLI skill](https://cooperemail.com/skills/cooper-email-cli/SKILL.md)
- [Cooper Email pricing](https://cooperemail.com/pricing)

## Skill Output:

**Output Type(s):** [API calls, Shell commands, Configuration instructions, Email and inbox data]

**Output Format:** [Markdown guidance with HTTP, MCP, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can retrieve inbox information or perform email actions through a connected Cooper inbox.]

## Skill Version(s):

1.0.0 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
