## Description:

Access 100+ AI tools via MCP \u2014 image generation, article writing, logo creation, SEO analysis, math solving, video generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adivyas99](https://clawhub.ai/user/adivyas99)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to connect an OpenClaw agent to AADDYY's MCP server for content generation, image and video creation, SEO analysis, education tools, and related pay-per-use AI utilities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs and runs a third-party MCP server that can receive prompts, files, URLs, and an AADDYY API key.

Mitigation: Use a dedicated revocable AADDYY API key with spending limits, avoid confidential inputs unless approved, and review the MCP package before deployment.

Risk: The MCP package is not pinned in the setup command, so future installs may pull changed server behavior.

Mitigation: Pin and review a specific MCP package version before using the skill in controlled or production environments.

Risk: Pay-per-use tools may consume paid AADDYY credits.

Mitigation: Monitor credit usage, set spending controls where available, and test workflows with low-risk prompts before broader use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/adivyas99/skills/aaddyy-ai-tools)
- [AADDYY documentation](https://www.aaddyy.com/docs)
- [AADDYY MCP server package](https://www.npmjs.com/package/@aaddyy/mcp-server)
- [AADDYY OpenAPI specification](https://backend.aaddyy.com/openapi.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Images, Video]

**Output Format:** [Markdown, shell commands, configuration snippets, and tool-generated media or analysis]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires npx and AADDYY_API_KEY; tool calls consume AADDYY credits unless the selected tool is free.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
