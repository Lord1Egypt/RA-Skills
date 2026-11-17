## Description:

AI电商专家｜电商图片视频全套生成 helps ecommerce operators, designers, and brand marketing teams prepare IMIVA MCP workflows for product images, detail pages, and videos from product assets, verified selling points, channel goals, and output specifications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce content teams use this skill to turn product materials, confirmed selling points, target audiences, channel requirements, and budget limits into executable IMIVA MCP media-generation tasks. It supports product main images, detail-page assets, ecommerce videos, task lookup, and result review for marketplace listing and social-commerce workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to run a mutable npm MCP package with an IMIVA account token and broad local environment access.

Mitigation: Review the skill before installation, keep MCP_TOKEN in local secrets, avoid running it in environments containing unrelated API keys, and prefer a pinned, reviewed package version or restricted runtime where available.

Risk: Media generation tasks may spend account credits or cause duplicate charges if failed tasks are recreated without checking the original task.

Mitigation: Check credits before submission, confirm generation count and model settings, use dryRun or estimatedCredits for video, preserve task IDs, and query existing tasks before retrying.

Risk: Generated ecommerce assets can contain inaccurate product details, unsupported claims, or copied third-party creative elements.

Mitigation: Use only user-provided or confirmed product facts, confirm rights for reference media, avoid protected marks or personas, and review output accuracy before publication.

## Reference(s):

- [IMIVA homepage](https://imiva.ecpro.com/)
- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/ai-ecommerce-expert-ecommerce-image-video-suite)
- [IMIVA MCP configuration example](artifact/references/mcp-config.example.json)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration, code]

**Output Format:** [Markdown guidance with JSON configuration and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses IMIVA MCP task IDs, account credits, local file paths or HTTPS asset URLs, and model-specific image/video settings.]

## Skill Version(s):

1.0.0 (source: server release, target metadata, and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
