## Description:

AI电商专家｜TikTok Shop 图片视频全内容 helps TikTok Shop merchants, operators, designers, ad teams, and agencies prepare IMIVA ecommerce content workflows for product images, detail content, and video assets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce teams use this skill to structure TikTok Shop listing, seeding, advertising, and conversion-oriented content generation requests for IMIVA MCP tools. It helps collect product facts, assets, specifications, budget confirmation, task creation, task lookup, and output review steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs a mutable npm package with an MCP token and inherited environment access.

Mitigation: Use a reviewed pinned package version where possible, provide a narrowly scoped revocable token, and run it in an environment without unrelated secrets.

Risk: Changing the API endpoint or using untrusted ecommerce generation tasks could expose credentials or route work to an unintended service.

Mitigation: Keep the API endpoint on the official HTTPS host and invoke the tool only for explicit IMIVA ecommerce generation tasks.

Risk: Generated ecommerce content can misstate product facts or misuse third-party creative material.

Mitigation: Use only user-confirmed product claims and review referenced competitor or viral materials for authorization before publication.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/ai-ecommerce-expert-tiktok-shop-ecommerce-content)
- [IMIVA homepage](https://imiva.ecpro.com/)
- [MCP configuration example](references/mcp-config.example.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with JSON and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose IMIVA MCP calls and configuration steps; generated media tasks require user-provided credentials and budget confirmation.]

## Skill Version(s):

1.0.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
