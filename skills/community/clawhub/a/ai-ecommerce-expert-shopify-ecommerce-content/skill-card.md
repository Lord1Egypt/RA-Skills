## Description:

AI电商专家｜Shopify 独立站 图片视频全内容 helps Shopify and DTC ecommerce teams use IMIVA MCP workflows to prepare product images, detail-page content, seeding assets, advertising creatives, and video materials from confirmed product inputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External Shopify, DTC, brand, operations, design, advertising, and agency teams use this skill to turn product materials, audience goals, channel requirements, and budget constraints into IMIVA MCP task calls for ecommerce images, detail pages, and videos.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The MCP helper runs an external npm package published as @latest with the user's MCP token and inherited environment variables.

Mitigation: Use a pinned, reviewed package version where possible and run it from an environment that contains only the required MCP token and API URL.

Risk: Generation calls can consume credits or create unwanted assets if task details are submitted without confirmation.

Mitigation: Confirm model, quantity, resolution, budget, source asset rights, and task parameters before creating paid generation tasks.

Risk: Generated ecommerce claims, product visuals, pricing, certifications, or comparisons may be inaccurate or unsupported.

Mitigation: Use only user-confirmed product facts and review generated assets against channel requirements before publication.

## Reference(s):

- [IMIVA homepage](https://imiva.ecpro.com/)
- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/ai-ecommerce-expert-shopify-ecommerce-content)
- [MCP configuration example](references/mcp-config.example.json)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, API calls, Markdown, JSON]

**Output Format:** [Markdown guidance with JSON arguments, MCP configuration snippets, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May submit IMIVA MCP generation tasks that return task IDs and generated ecommerce image, detail-page, or video assets through the external IMIVA service.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
