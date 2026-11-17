## Description:

AI电商专家｜抖音电商 图片视频全内容 helps ecommerce merchants, operations, design, advertising, and agency teams prepare IMIVA MCP tasks for Douyin product images, product-detail content, seeding assets, and video creatives.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce merchants, brand teams, content operators, designers, performance marketers, and agencies use this skill to turn product materials, channel goals, budgets, and specifications into executable IMIVA MCP calls for Douyin ecommerce image, detail-page, and video content production.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs a mutable external npm MCP package and can inherit unrelated environment variables.

Mitigation: Use a pinned and reviewed MCP package version where possible, run it with a minimized environment allowlist, and keep unrelated secrets out of the execution environment.

Risk: Product materials, prompts, and generated-content requests are sent to IMIVA.

Mitigation: Use the skill only where sending those materials to IMIVA is acceptable, and avoid including confidential or unauthorized third-party assets.

Risk: Paid image or video generation tasks may consume credits if submitted without preflight checks.

Mitigation: Check user credits, use dry runs for video estimates, require explicit budget confirmation, and preserve task IDs to avoid duplicate submissions.

## Reference(s):

- [IMIVA AI Ecommerce Expert](https://imiva.ecpro.com/)
- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/ai-ecommerce-expert-douyin-ecommerce-content)
- [MCP configuration example](artifact/references/mcp-config.example.json)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, API Calls]

**Output Format:** [Markdown guidance with JSON configuration examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs guide MCP setup, credit checks, dry runs, task creation, task lookup, and ecommerce content quality review.]

## Skill Version(s):

1.0.0 (source: server release evidence and SKILL.md metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
