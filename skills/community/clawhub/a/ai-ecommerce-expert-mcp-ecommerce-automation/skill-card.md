## Description:

AI电商专家｜MCP 电商内容自动化 helps developers, ecommerce operators, agent teams, and enterprise content teams connect IMIVA through MCP to query products, prepare content tasks, check credits, track task progress, and manage ecommerce image and video deliverables.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, ecommerce operations teams, AI agent builders, and enterprise content teams use this skill to automate IMIVA-backed ecommerce content workflows for product images, detail pages, social commerce assets, product videos, and task delivery tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs an unpinned external npm package while using a live MCP token.

Mitigation: Install only if the IMIVA npm package is trusted, ask the publisher to pin the package version before production use, and run it in a clean shell or container.

Risk: The MCP process can receive more environment data than it needs.

Mitigation: Provide only MCP_TOKEN, API_URL, and PATH to the runtime environment, and keep the full token out of skills, screenshots, chat logs, and repositories.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/ai-ecommerce-expert-mcp-ecommerce-automation)
- [IMIVA homepage](https://imiva.ecpro.com/)
- [MCP configuration example](references/mcp-config.example.json)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration, API calls, JSON]

**Output Format:** [Markdown with inline bash and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a user-provided MCP token and confirmed product facts, budget, model, and channel requirements before creating paid content tasks.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
