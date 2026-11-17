## Description:

AI电商专家｜食品饮料电商图片视频 helps food and beverage ecommerce brands, merchants, operators, designers, advertising teams, and content teams use IMIVA MCP workflows to create product listing images, detail-page assets, seeding content, and product video materials.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce teams and content operators use this skill to structure IMIVA MCP requests for food and beverage product images, detail pages, social seeding assets, marketplace listings, and product videos. The workflow emphasizes preserving product facts, confirming budget and credits, submitting MCP tasks, and checking generated outputs against channel requirements.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence reports that the skill runs an unpinned remote npm package and forwards the full local environment to it.

Mitigation: Use a pinned package version, run it in a restricted environment, and avoid invoking it from shells that contain unrelated cloud, repository, or production secrets.

Risk: The skill requires an MCP token for IMIVA operations and may submit chargeable content-generation tasks.

Mitigation: Use a narrowly scoped revocable MCP token, check credits or dry-run estimates where available, and obtain budget confirmation before creating tasks.

## Reference(s):

- [IMIVA homepage](https://imiva.ecpro.com/)
- [MCP config example](references/mcp-config.example.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON configuration examples and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides agents to collect product facts, prepare MCP task arguments, confirm budgets, query task status, and review generated ecommerce content.]

## Skill Version(s):

1.0.0 (source: server release evidence and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
