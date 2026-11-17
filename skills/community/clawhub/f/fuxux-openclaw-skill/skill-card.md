## Description:

Enables OpenClaw agents to draft, schedule, publish, edit, and review social media content across 14 platforms through Fuxux REST API and MCP.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abogitoff](https://clawhub.ai/user/abogitoff)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users can use Fuxux to prepare platform-specific captions, save drafts, schedule or publish posts to connected social accounts, manage queued content, and review publishing analytics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A compromised or exposed FUXUX_API_KEY could allow access to connected accounts and social media actions.

Mitigation: Protect the key as a password, store it securely, and rotate it if it is exposed.

Risk: Posts may be published to connected social accounts, and uploaded media is publicly accessible.

Mitigation: Connect only accounts intended for management, use drafts to review content before publishing, and avoid uploading media that should remain private.

Risk: The optional stdio MCP bridge adds a third-party package to the connection path.

Mitigation: Prefer the direct HTTP MCP endpoint or review and pin the bridge version before use.

## Reference(s):

- [Fuxux OpenClaw guide](https://www.fuxux.com/openclaw)
- [Fuxux MCP setup guide](https://www.fuxux.com/mcp/docs)
- [Fuxux API reference](https://www.fuxux.com/reference)
- [Fuxux OpenAPI specification](https://www.fuxux.com/openapi.json)

## Skill Output:

**Output Type(s):** [Text, Guidance, Configuration, API calls]

**Output Format:** [Platform-specific captions and post content, scheduling and publishing actions, analytics summaries, and JSON MCP configuration.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Content can be saved as drafts for review or scheduled for connected social accounts.]

## Skill Version(s):

1.1.6 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
