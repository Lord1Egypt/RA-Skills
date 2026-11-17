## Description:

This skill helps AliExpress sellers and ecommerce teams turn product assets, verified selling points, channel goals, and output specs into IMIVA MCP tasks for product images, detail content, and video materials.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce sellers, operators, designers, ad teams, and agency teams use this skill to prepare IMIVA ecommerce content-generation tasks for AliExpress listings, product visuals, detail pages, KOC or UGC seeding, and product videos. The skill is also useful for agents that need guided shell commands, MCP configuration, task arguments, and result-checking workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs an unpinned external IMIVA MCP package through npx.

Mitigation: Pin and review the package version before production use, and install only when the IMIVA service and npm package supply chain are trusted.

Risk: The skill uses broad environment access for MCP_TOKEN and API_URL.

Mitigation: Run it in an isolated environment with only the required environment variables and avoid storing tokens in skill files, screenshots, chats, or repositories.

Risk: Implicit invocation is enabled and ecommerce generation tasks may consume credits or send product assets.

Mitigation: Disable implicit invocation where possible and require user confirmation for assets, model choices, estimated credits, and task creation.

## Reference(s):

- [IMIVA homepage](https://imiva.ecpro.com/)
- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/ai-ecommerce-expert-aliexpress-ecommerce-content)
- [MCP configuration example](references/mcp-config.example.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON MCP arguments, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an IMIVA MCP token for live tool calls; generated tasks may consume credits and should be confirmed before submission.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
