## Description:

AI电商专家｜Instagram INS 电商 图片视频全内容 helps ecommerce merchants, operators, designers, advertisers, and agency teams use IMIVA MCP workflows to generate product images, detail-page content, KOC seeding packages, and video assets for Instagram, INS, Instagram Shop, Reels, Stories, and Meta Ads.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce merchants, brand operators, designers, advertisers, and agency teams use this skill to turn verified product materials, selling points, target audiences, channel goals, and budget constraints into executable IMIVA MCP content-generation tasks. It supports product listing, social commerce seeding, advertising creative, detail-page content, task tracking, and result review for Instagram-oriented ecommerce workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs a mutable npm MCP package with access to the MCP token and the agent process environment.

Mitigation: Use a pinned reviewed package version where possible, run it in a low-secret environment, and keep the MCP token in environment variables or a client secret store.

Risk: Broad API_URL overrides or token handling mistakes could expose requests or credentials to an unintended endpoint.

Mitigation: Use the default IMIVA endpoint unless there is a reviewed reason to override it, and do not write tokens into skill files, screenshots, chat logs, or repositories.

Risk: Image or video generation tasks may consume paid credits when submitted.

Mitigation: Check credits first, use dry-run budget estimates where available, confirm the generation count, model, and maximum budget with the user, and retain task IDs to avoid duplicate submissions.

Risk: Generated ecommerce content can include unsupported product claims or improperly reuse third-party creative elements.

Mitigation: Use only user-provided or confirmed product facts, verify prices, certifications, effects, and comparisons before publication, and confirm authorization before adapting competitor or viral reference material.

## Reference(s):

- [IMIVA homepage](https://imiva.ecpro.com/)
- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/ai-ecommerce-expert-instagram-ecommerce-content)
- [MCP configuration example](references/mcp-config.example.json)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, JSON, markdown]

**Output Format:** [Markdown guidance with JSON MCP arguments and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include task IDs, credit-check guidance, MCP configuration snippets, content-generation parameters, and review checklists.]

## Skill Version(s):

1.0.0 (source: server evidence release.version and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
