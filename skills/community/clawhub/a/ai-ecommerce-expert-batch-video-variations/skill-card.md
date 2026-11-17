## Description:

AI电商专家｜批量商品视频变体 helps ecommerce content, advertising, operations, brand, and social commerce teams plan and submit batches of product video variants through IMIVA MCP for creative testing, channel adaptation, and multi-SKU content production.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce teams and operators use this skill to turn product assets, channel goals, audience details, and budget constraints into IMIVA video-generation task parameters. It supports batch product video variation workflows, including dry-run credit checks, paid task submission after confirmation, task lookup, and result review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses an external npm MCP package and requires an MCP token, which creates supply-chain and credential exposure risk.

Mitigation: Install only when the IMIVA package source is trusted, use a narrowly scoped and revocable token, and avoid running it from shells that contain unrelated secrets.

Risk: Paid video-generation tasks can consume credits if submitted without checking estimated cost.

Mitigation: Use an explicit dry run and require budget confirmation before creating paid video tasks.

Risk: A generic API_URL environment variable can accidentally route requests to an unintended endpoint.

Mitigation: Prefer an explicit IMIVA endpoint configuration and verify the target service before submitting tasks.

## Reference(s):

- [IMIVA homepage](https://imiva.ecpro.com/)
- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/ai-ecommerce-expert-batch-video-variations)
- [Publisher profile](https://clawhub.ai/user/wubin1836)
- [MCP configuration example](references/mcp-config.example.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON configuration examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include MCP task arguments, dry-run budget checks, task IDs, and review guidance for generated ecommerce video outputs.]

## Skill Version(s):

1.0.0 (source: server release evidence and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
