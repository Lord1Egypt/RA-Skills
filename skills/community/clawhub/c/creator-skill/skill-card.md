## Description:

Creator SKILL searches TikTok, Instagram, and YouTube influencers through the Deinai MCP using natural-language criteria, structured filters, and location resolution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deinai](https://clawhub.ai/user/deinai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to discover creators, KOLs, and influencers on TikTok, Instagram, and YouTube by niche, platform, follower range, language, location, public email availability, or creator handle.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: MCP bearer tokens can be exposed through command-line configuration, shell history, logs, or screenshots.

Mitigation: Use the shortest practical token expiry, avoid exposing the token in visible commands or screenshots, and rotate the token immediately if it may have been exposed.

Risk: Influencer searches consume team credits based on the number of records returned.

Mitigation: Confirm broad or large searches before running searchInfluencers, use specific filters, and choose a practical page_size.

Risk: A normal user login JWT may be confused with the required MCP token.

Mitigation: Create and configure the dedicated MCP bearer token from the Deinai token endpoint before connecting the MCP server.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/deinai/skills/creator-skill)
- [Deinai production API](https://deinai.ai)
- [Deinai MCP endpoint](https://deinai.ai/mcp)
- [Installation and authentication](references/install.md)
- [MCP tools](references/tools.md)
- [Errors and handling](references/errors.md)
- [Tool contract](tool_specs.yaml)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, API calls]

**Output Format:** [Markdown guidance with MCP tool calls, JSON configuration snippets, and plain-text search results.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Deinai account, MCP bearer token, and team search credits; searchInfluencers returns up to 50 records per page.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
