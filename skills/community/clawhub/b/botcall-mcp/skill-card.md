## Description:

Give your AI agent a real phone number for SMS verification. Provisions numbers, receives SMS, and extracts verification codes via the botcall API. Requires a BOTCALL_API_KEY from botcall.io.

This skill is ready for commercial/non-commercial use.

## Publisher:

[danecodes](https://clawhub.ai/user/danecodes)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this MCP server to provision phone numbers, retrieve SMS messages, and extract verification codes for accounts and services they are authorized to verify.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives an agent access to phone-number provisioning, SMS messages, and verification codes, which can expose sensitive account verification material.

Mitigation: Use it only for accounts and services the user is authorized to verify, and treat SMS contents and verification codes as sensitive.

Risk: The documented setup installs an unpinned third-party MCP package.

Mitigation: Prefer a pinned or otherwise vetted package version before deployment.

Risk: Botcall API usage may incur plan charges and relies on an API key.

Mitigation: Monitor Botcall plan usage and avoid storing broad or long-lived API keys in configuration files.

## Reference(s):

- [botcall.io](https://botcall.io)
- [botcall-mcp npm package](https://www.npmjs.com/package/botcall-mcp)
- [ClawHub skill page](https://clawhub.ai/danecodes/skills/botcall-mcp)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide installation of an unpinned third-party MCP package and handling of sensitive SMS verification content.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
