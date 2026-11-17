## Description:

Social media scheduler, cross-poster, and content calendar for OpenClaw across YouTube, Instagram, Facebook, X, TikTok, Threads, and Pinterest.

This skill is ready for commercial/non-commercial use.

## Publisher:

[codivion](https://clawhub.ai/user/codivion)

### License/Terms of Use:

MIT-0

## Use Case:

External users, creators, agencies, and developers use this skill to help an OpenClaw agent schedule, publish, cross-post, and analyze social media content through the CodivUpload API. It is useful for managing content calendars, platform-specific post formats, bulk uploads, and livestream workflows from agent-generated guidance, commands, or API calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can affect real public social media accounts through the configured CodivUpload API key.

Mitigation: Use a single-platform or per-workspace API key where possible, avoid global account keys unless needed, and review every publish, bulk, livestream, delete, and billing approval prompt before execution.

Risk: Unpinned MCP or package execution in a credentialed environment could expose CODIVUPLOAD_API_KEY to unexpected code.

Mitigation: Use the exact pinned codivupload-mcp version and avoid unpinned npx or package install commands in the same environment as the API key.

Risk: Scheduled posts and livestreams may continue after the original agent session ends.

Mitigation: Prefer draft or scheduled workflows for review, track created post or stream identifiers, and explicitly cancel scheduled posts or stop livestreams when no longer intended.

## Reference(s):

- [CodivUpload Skill on ClawHub](https://clawhub.ai/codivion/skills/codivupload-social-manager)
- [CodivUpload Website](https://codivupload.com)
- [CodivUpload API Documentation](https://docs.codivupload.com)
- [CodivUpload OpenAPI Specification](https://api.codivupload.com/public-openapi.json)
- [CodivUpload MCP Server](https://www.npmjs.com/package/codivupload-mcp)
- [CodivUpload TypeScript SDK](https://www.npmjs.com/package/codivupload)
- [CodivUpload Python SDK](https://pypi.org/project/codivupload/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, API examples, and structured guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose CodivUpload REST API calls, SDK snippets, MCP usage, and OpenClaw configuration steps for user review.]

## Skill Version(s):

1.0.17 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
