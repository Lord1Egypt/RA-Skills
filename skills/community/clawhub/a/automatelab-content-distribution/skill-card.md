## Description:

Use when the user wants to publish a post, article, or announcement to multiple platforms at once: DEV.to, Hashnode, GitHub Discussions, Reddit, Bluesky, LinkedIn, Medium, or Twitter/X.

This skill is ready for commercial/non-commercial use.

## Publisher:

[automatelab](https://clawhub.ai/user/automatelab)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and content teams use this skill to draft platform-specific variants and publish or schedule the same announcement across multiple social and developer channels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup uses an unpinned external npm MCP server that can change after review.

Mitigation: Pin the MCP package version where possible and review package updates before deployment.

Risk: The MCP server handles posting credentials for connected platforms.

Mitigation: Run it with only the platform credentials intended for the current release workflow and verify credentials before publishing.

Risk: Content may be published or scheduled to unintended platforms or include private information.

Mitigation: Avoid private or secret content in posts and confirm every target platform and scheduled post before allowing publication.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/automatelab/skills/automatelab-content-distribution)
- [Content Distribution MCP repository](https://github.com/AutomateLab-tech/content-distribution-mcp)
- [Content Distribution MCP configuration](https://github.com/AutomateLab-tech/content-distribution-mcp#configuration)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON configuration examples and structured MCP tool calls]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce platform-specific copy variants, scheduling instructions, status checks, and retry guidance.]

## Skill Version(s):

2.2.1 (source: release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
