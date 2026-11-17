## Description:

AI电商专家｜Amazon A+ 页面 图片视频全内容 helps ecommerce merchants and content teams prepare and run IMIVA MCP workflows for Amazon A+ product-detail images, page copy, and video assets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce merchants, Amazon sellers, operations, design, advertising, and agency teams use this skill to turn product materials, verified selling points, target channels, and budget constraints into IMIVA MCP task parameters for Amazon A+ images, page content, and video assets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence says the skill automatically runs an unpinned npm package with the user's IMIVA token and inherited environment.

Mitigation: Use only after trusting the IMIVA package publisher, prefer a pinned package version, pass a minimal allowlisted environment, and use scoped, rotatable tokens.

Risk: Generation tasks may spend platform credits when submitted.

Mitigation: Confirm model, quantity, resolution, duration, maxCredits, and budget before creating tasks; use dry runs where supported and keep task IDs for follow-up instead of resubmitting blindly.

Risk: Generated ecommerce assets can become misleading if product facts, claims, or reference-material rights are not verified.

Mitigation: Use only user-confirmed product details and authorized source material, then review text, claims, logos, packaging, and channel requirements before publication.

## Reference(s):

- [IMIVA homepage](https://imiva.ecpro.com/)
- [ClawHub skill listing](https://clawhub.ai/wubin1836/skills/ai-ecommerce-expert-amazon-a-plus-ecommerce-content)
- [MCP configuration example](references/mcp-config.example.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON configuration examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can prepare MCP task arguments and task-query commands; generation results come from the IMIVA service after user token, material, budget, and task details are confirmed.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
