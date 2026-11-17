## Description:

AI电商专家｜电商全内容一站式生成 helps ecommerce teams prepare IMIVA MCP requests for product images, detail pages, KOC content, marketing visuals, product videos, task checks, and result delivery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce merchants, brand teams, operations agencies, designers, and content teams use this skill to turn product assets, channel goals, selling points, budgets, and output specs into IMIVA MCP workflows for commercial ecommerce content generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs an unpinned npm MCP package with a user token and inherited environment.

Mitigation: Prefer a pinned MCP package version, keep the token in a minimal allowlisted environment, and review the package before installation.

Risk: Generation tasks may spend credits or send local product assets to IMIVA.

Mitigation: Confirm model, quantity, resolution, credit budget, and asset sharing with the user before creating billable tasks.

Risk: Generated ecommerce content can misstate product facts or reuse protected third-party creative elements.

Mitigation: Use only user-confirmed product claims and review outputs for factual accuracy, authorization, channel fit, and intellectual-property risk before publication.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/ai-ecommerce-expert-ecommerce-content-studio)
- [Publisher profile](https://clawhub.ai/user/wubin1836)
- [IMIVA homepage](https://imiva.ecpro.com/)
- [MCP configuration example](references/mcp-config.example.json)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration, API calls]

**Output Format:** [Markdown with JSON configuration and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May submit or query IMIVA MCP tasks when configured with a valid MCP token.]

## Skill Version(s):

1.0.0 (source: server evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
