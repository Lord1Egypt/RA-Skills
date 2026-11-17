## Description:

帮助服装时尚品牌和电商团队通过 IMIVA MCP 将商品素材、卖点、渠道和规格整理为可执行任务，生成可上架或投放的商品主图、详情页素材、种草内容和视频素材。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce brands, merchants, operators, designers, advertising teams, and content teams use this skill to prepare IMIVA MCP tasks for apparel and fashion product images, detail pages, KOC seeding content, product videos, and marketplace or social-commerce creatives. The workflow emphasizes user-confirmed product facts, budget checks, task tracking, and channel-specific review before publishing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs a mutable npm MCP package with an MCP token and the full parent environment.

Mitigation: Use a narrowly scoped, revocable MCP token, run it from an environment without unrelated secrets, and prefer a pinned or preinstalled CLI version before business use.

Risk: Selected product assets are sent to IMIVA for image and video generation.

Mitigation: Submit only assets the user is authorized to process and is comfortable sending to IMIVA; avoid unrelated secrets, confidential files, and unlicensed third-party materials.

Risk: Generated ecommerce content can contain inaccurate product claims, text errors, or unauthorized brand, person, or creative elements.

Mitigation: Review generated outputs against user-confirmed product facts, channel requirements, and asset permissions before publishing or using them in advertising.

## Reference(s):

- [IMIVA AI电商专家官网](https://imiva.ecpro.com/)
- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/ai-ecommerce-expert-apparel-fashion-ecommerce-content)
- [MCP configuration example](references/mcp-config.example.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses IMIVA MCP task IDs and user-supplied product assets for traceable ecommerce content generation workflows.]

## Skill Version(s):

1.0.0 (source: SKILL.md metadata, ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
