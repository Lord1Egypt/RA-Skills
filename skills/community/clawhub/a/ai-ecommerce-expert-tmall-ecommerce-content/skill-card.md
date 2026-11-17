## Description:

AI电商专家｜天猫 图片视频全内容 helps Tmall merchants and ecommerce content teams prepare IMIVA MCP tasks for product images, detail pages, seeding content, ad creatives, and product videos.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External Tmall merchants, ecommerce operators, designers, ad teams, and agency teams use this skill to structure commercial image, detail-page, seeding, advertising, and product-video generation requests for IMIVA. It helps users confirm source assets, product facts, specifications, budget, task submission, result tracking, and channel-oriented review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs a mutable external npm MCP package that receives the user's MCP token and may inherit environment variables.

Mitigation: Install only when the IMIVA package is trusted, prefer a pinned package version, and run with a minimal environment containing only required credentials.

Risk: Image and video generation tasks may consume paid credits when submitted.

Mitigation: Confirm model, count, duration, resolution, and budget before creating tasks; use dry-run credit estimates where supported and retain task IDs for follow-up queries.

Risk: Permissive implicit invocation can broaden when the skill is used beyond specific Tmall ecommerce tasks.

Mitigation: Prefer explicit invocation for defined Tmall workflows and review generated MCP parameters before submitting tasks.

## Reference(s):

- [IMIVA AI Ecommerce Expert](https://imiva.ecpro.com/)
- [ClawHub Skill Release](https://clawhub.ai/wubin1836/skills/ai-ecommerce-expert-tmall-ecommerce-content)
- [MCP configuration example](references/mcp-config.example.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON configuration and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce IMIVA MCP task parameters, task IDs, status-query commands, and result-delivery guidance when the MCP package is configured.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
