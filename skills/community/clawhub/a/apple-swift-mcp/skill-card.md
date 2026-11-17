## Description:

This skill helps users work with Apple app data through a native Swift MCP server on macOS.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrischall](https://clawhub.ai/user/chrischall)

### License/Terms of Use:

MIT-0

## Use Case:

Mac users use the skill to search and manage Calendar, Reminders, Contacts, Maps, Mail, Messages, Notes, Photos, and Music playlists through the server's tools. It requires macOS 27.2 or later on Apple Silicon.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access sensitive Apple app data and includes tools that send, edit, or delete data.

Mitigation: Grant only the macOS permissions needed for intended tasks, prefer read-only tools where possible, and review confirmation previews before approving writes.

Risk: Some referenced content was unavailable to the security scanners, leaving the review evidence incomplete.

Mitigation: Review the linked project and release materials before installing, and confirm the requested permissions match your intended use.

## Reference(s):

- [apple-swift-mcp project](https://github.com/chrischall/apple-swift-mcp)
- [apple-swift-mcp releases](https://github.com/chrischall/apple-swift-mcp/releases)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [Structured JSON and text responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the selected tool, operation, permissions, and requested data.]

## Skill Version(s):

2.11.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
