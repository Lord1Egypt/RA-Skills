## Description:

AI电商专家｜电商文生视频 helps ecommerce content, advertising, operations, brand, livestream, and seeding teams use IMIVA MCP to turn product scripts and selling points into commercial short videos.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce, brand, agency, and content teams use this skill to prepare IMIVA MCP requests for text-to-video product advertising workflows, including budget checks, video generation, task lookup, and output review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs an unpinned npm MCP package at runtime with the user's IMIVA token and inherited environment.

Mitigation: Use a dedicated IMIVA token, avoid running from environments that contain unrelated secrets, and prefer a pinned or locally vetted MCP package version before production use.

Risk: Non-dry-run video generation can consume platform credits or incur cost.

Mitigation: Run dry-run checks first, review estimated credits, and require explicit user confirmation for maxCredits and the final task submission.

Risk: Generated ecommerce videos can misstate product facts or reuse material without sufficient rights.

Mitigation: Use only user-provided or confirmed product claims and authorized assets, then review the generated video for accuracy, branding, text, and channel suitability before publishing.

## Reference(s):

- [IMIVA homepage](https://imiva.ecpro.com/)
- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/ai-ecommerce-expert-ecommerce-text-to-video)
- [MCP configuration example](references/mcp-config.example.json)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration, API calls]

**Output Format:** [Markdown with JSON and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include IMIVA MCP task arguments, dry-run credit checks, task IDs, and video review criteria.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
