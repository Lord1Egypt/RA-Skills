## Description:

AI电商专家｜电商商品详情页 helps ecommerce creative, operations, photography, brand, and advertising teams prepare IMIVA MCP requests that generate structured product-detail-page image sets from 1 to 5 product images and verified selling points.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce teams use this skill to turn product images, verified selling points, channel goals, and output specifications into IMIVA MCP task parameters for product detail page generation. It also guides token setup, budget confirmation, task tracking, and result review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs an unpinned npm MCP package with user credentials and inherited environment access.

Mitigation: Use a pinned, reviewed package version, run it in a clean environment without unrelated secrets, and rotate the MCP token if exposure is suspected.

Risk: The MCP token may create chargeable IMIVA tasks.

Mitigation: Check credits and confirm model, quantity, resolution, and budget before submitting generation tasks.

Risk: Overriding API_URL or IMIVA_API_URL to an untrusted host could expose credentials or task data.

Mitigation: Keep the default IMIVA endpoint unless the alternate host is trusted and explicitly approved.

## Reference(s):

- [IMIVA AI Ecommerce Expert](https://imiva.ecpro.com/)
- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/ai-ecommerce-expert-ecommerce-detail-page)
- [MCP configuration example](references/mcp-config.example.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline JSON and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces IMIVA MCP task parameters and workflow guidance; generated media is produced by the external IMIVA service.]

## Skill Version(s):

1.0.0 (source: evidence.json, release metadata, and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
