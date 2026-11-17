## Description:

Sign in to the Finance District agent wallet when a user needs to log in, connect, configure the wallet, or recover from authentication errors before wallet operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rachidjarray-hk-qa-fdt](https://clawhub.ai/user/rachidjarray-hk-qa-fdt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and users working with the Finance District agent wallet use this skill to check authentication status, start browser or device OAuth setup, handle common token errors, and log out when needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores wallet authentication state locally, and that auth file may grant wallet access while tokens remain valid.

Mitigation: Treat the local auth file as sensitive and use fdx logout when the agent wallet should no longer remain signed in.

Risk: A user could authorize an unexpected OAuth destination during setup.

Mitigation: Confirm the authorization or verification URL is expected before completing browser or device authorization.

## Reference(s):

- [Authenticate skill page](https://clawhub.ai/rachidjarray-hk-qa-fdt/skills/authenticate)
- [Finance District MCP server](https://mcp.fd.xyz)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and environment variable guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide a human through browser or device OAuth authorization and references local token storage.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
