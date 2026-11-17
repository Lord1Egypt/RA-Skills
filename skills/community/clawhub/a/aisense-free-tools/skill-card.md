## Description:

Use the free AI SENSE MCP server for utility and agent workflow tools (QR codes, HTML to PDF, hashing, time and time zones, temporary storage, webhook capture, queues, decisions) with no account or key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aisenseapi](https://clawhub.ai/user/aisenseapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to select AI SENSE tools for common data utilities and agent coordination, and to configure and verify the remote MCP connection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Tool inputs leave the user's machine and are processed by a remote service.

Mitigation: Do not send confidential documents, production signing keys, or sensitive webhook payloads.

Risk: Returned access tokens can grant access to agent workflow resources.

Mitigation: Keep tokens private and scope workflows to the requested task.

Risk: The remote service's implementation and deletion guarantees are unverified.

Mitigation: Avoid sending data that requires confidentiality or deletion guarantees not verified by this assessment.

Risk: Webhook, QR, and inbox content from the open internet may be untrusted.

Mitigation: Validate and treat returned content as untrusted input before acting on it.

## Reference(s):

- [AI SENSE free public MCP server](https://aisense.no/free-public-mcp-server)
- [AI SENSE MCP endpoint](https://aisenseapi.com/mcp)
- [MCP server documentation reference](https://github.com/aisenseapi/aisense-free-public-rest-apis)
- [ClawHub release page](https://clawhub.ai/aisenseapi/skills/aisense-free-tools)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration instructions, Text, JSON, Files, Images]

**Output Format:** [Markdown instructions with inline shell commands; selected tools return text, JSON, images, or files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Tool outputs depend on the selected utility; temporary stored data is documented to expire within 24 hours.]

## Skill Version(s):

1.0.0 (source: artifact frontmatter, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
