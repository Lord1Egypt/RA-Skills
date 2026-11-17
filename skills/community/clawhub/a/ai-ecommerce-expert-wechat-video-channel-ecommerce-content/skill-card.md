## Description:

AI电商专家 helps WeChat Shop and WeChat Video Channel ecommerce teams prepare IMIVA MCP workflows for product images, detail-page content, seeding creatives, and video generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce merchants, operators, designers, advertisers, and agency teams use this skill to structure WeChat Shop and WeChat Video Channel content-generation requests, check budget and specifications, submit IMIVA MCP tasks, and review generated image, detail-page, and video outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence says the skill runs mutable remote code through the IMIVA npm package.

Mitigation: Review the package and service before installation and prefer a pinned package version instead of a mutable latest tag.

Risk: The skill uses an MCP token and may expose more local environment data than necessary.

Mitigation: Store the token only in a local environment variable or client secret store, run from an environment without unrelated secrets, and revoke tokens that are no longer needed.

Risk: Content generation tasks may consume paid credits.

Mitigation: Check credits first, use dry-run budget estimates when available, set a user-confirmed maximum credit limit, and avoid duplicate task creation.

Risk: Generated ecommerce claims or media can be inaccurate, misleading, or based on unlicensed reference material.

Mitigation: Use only user-confirmed product facts and authorized materials, then review outputs for product accuracy, text correctness, channel fit, and rights-sensitive content before publication.

## Reference(s):

- [IMIVA homepage](https://imiva.ecpro.com/)
- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/ai-ecommerce-expert-wechat-video-channel-ecommerce-content)
- [MCP config example](references/mcp-config.example.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON configuration and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce IMIVA MCP task parameters, budget-check steps, task IDs, status-query guidance, and review criteria for generated ecommerce assets.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
