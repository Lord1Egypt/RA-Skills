## Description:

Control Ecovacs robot vacuums through the official Ecovacs MCP server to list devices, start, pause, resume, or stop cleaning, send a robot to its dock, and check battery, cleaning, charging, and station status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[f-liva](https://clawhub.ai/user/f-liva)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an assistant operate Ecovacs DEEBOT robot vacuums through an MCP server, including cleaning control, docking, device discovery, and status checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The MCP server receives the user's Ecovacs API key.

Mitigation: Install only when the user is comfortable granting the server access to the Ecovacs account, and keep the API key in the configured environment variable rather than exposing it in conversation.

Risk: The skill can control a physical robot vacuum, including start, stop, pause, resume, and dock actions.

Mitigation: Confirm robot-specific intent before taking control actions, especially for short or ambiguous requests.

Risk: The configured MCP command runs the external ecovacs-robot-mcp package without a pinned package version.

Mitigation: Pin or otherwise verify the ecovacs-robot-mcp package before running it in production settings.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/f-liva/skills/ecovacs-mcp)
- [Ecovacs MCP Server](https://github.com/ecovacs-ai/ecovacs-mcp)
- [Ecovacs Open Platform](https://open.ecovacs.com)
- [Ecovacs China Open Platform](https://open.ecovacs.cn)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with JSON configuration and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide MCP tool calls that control a physical robot vacuum when the Ecovacs API key and MCP server are configured.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
