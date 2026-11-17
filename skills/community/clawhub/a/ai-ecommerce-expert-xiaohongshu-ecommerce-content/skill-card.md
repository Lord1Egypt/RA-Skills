## Description:

AI电商专家｜小红书电商 图片视频全内容 helps ecommerce merchants, operators, designers, advertisers, and agency teams prepare IMIVA MCP parameters for Xiaohongshu product images, detail content, KOC seeding notes, and video assets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce teams use this skill to turn product facts, source assets, channel goals, and budget constraints into executable IMIVA MCP calls for Xiaohongshu listings, seeding content, advertising creatives, and conversion-focused product media. It also guides task lookup and result review so users can avoid duplicate paid submissions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs a mutable external npm package and inherits local credentials through the MCP runtime.

Mitigation: Use a dedicated low-scope IMIVA token, avoid environments with unrelated secrets, and prefer a pinned, reviewed package version before production deployment.

Risk: MCP calls may create paid content-generation tasks or use a non-default endpoint.

Mitigation: Require explicit user confirmation before creating paid tasks, set budget limits where supported, and confirm any API endpoint override before use.

Risk: Generated ecommerce claims, prices, certifications, or visual details may be inaccurate or misleading.

Mitigation: Use only user-confirmed product facts and review generated media for product accuracy, text accuracy, authorization, and channel suitability before publication.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/ai-ecommerce-expert-xiaohongshu-ecommerce-content)
- [IMIVA homepage](https://imiva.ecpro.com/)
- [MCP configuration example](references/mcp-config.example.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON configuration examples and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include IMIVA MCP tool arguments, task identifiers, budget checks, and result-review guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
