## Description:

MCP skill for Canva that provides tools to upload assets, resolve shortlinks, search and retrieve designs, manage design pages and folders, export content, comment on designs, generate designs, and list brand kits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[manojbajaj95](https://clawhub.ai/user/manojbajaj95)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to connect an agent to Canva through MCP for searching, retrieving, creating, importing, exporting, commenting on, and organizing Canva content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can change Canva content through OAuth-backed actions such as uploads, imports, folder changes, comments, design generation, and page operations.

Mitigation: Review the requested action before execution and explicitly confirm destructive page operations, public comments, and content changes.

Risk: OAuth-backed requests may expose more chat context or Canva account content than intended.

Mitigation: Use only the default Canva MCP endpoint, avoid running the skill from chats containing secrets or unrelated private information, and revoke the stored OAuth token if access is no longer needed.

Risk: The security scan verdict is suspicious because the skill can modify Canva content and relies on a third-party dependency.

Mitigation: Review the skill before installing, consider pinning or reviewing the mcp-skill dependency, and limit use to Canva accounts and workspaces appropriate for agent access.

## Reference(s):

- [ClawHub Canva skill page](https://clawhub.ai/manojbajaj95/skills/canva-2)
- [Canva MCP endpoint](https://mcp.canva.com/mcp)

## Skill Output:

**Output Type(s):** [Text, JSON, URLs, Configuration, Guidance]

**Output Format:** [Structured tool results returned as JSON-like dictionaries, with text fields and URLs for Canva resources or exported files when provided by Canva.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [OAuth-backed MCP calls may read or modify Canva content depending on the selected tool and user authorization.]

## Skill Version(s):

0.1.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
