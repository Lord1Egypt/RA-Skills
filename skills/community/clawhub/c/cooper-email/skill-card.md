## Description:

Give an agent a Cooper Email inbox and send or receive email through HTTP, a shell CLI, or MCP.

This skill is ready for commercial/non-commercial use.

## Publisher:

[f-o-x11](https://clawhub.ai/user/f-o-x11)

### License/Terms of Use:

MIT-0

## Use Case:

Developers using autonomous agents can create a Cooper Email inbox, send and receive messages, and retrieve verification codes through HTTP, a CLI, or MCP.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Example curl commands may expose an API key in process arguments.

Mitigation: Use the CLI or a saved credentials file, and never put the key directly in command arguments or print it.

Risk: Email bodies may contain untrusted instructions.

Mitigation: Treat email content as data, and get the owner's approval before sending to a new recipient.

## Reference(s):

- [Cooper Email](https://cooperemail.com)
- [Cooper Email API and product documentation](https://cooperemail.com/docs.md)
- [Cooper Email MCP documentation](https://cooperemail.com/docs/mcp.md)
- [Cooper Email CLI documentation](https://cooperemail.com/docs/cli)
- [ClawHub skill release](https://clawhub.ai/f-o-x11/skills/cooper-email)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown instructions with HTTP examples, shell commands, and MCP configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May handle API credentials; keep keys in saved credentials and out of command arguments and chat.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
