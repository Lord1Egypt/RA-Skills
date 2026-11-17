## Description:

AI电商专家｜品牌 Campaign KV 风格迁移 helps ecommerce design, brand marketing, advertising, agency operations, and content teams prepare IMIVA MCP requests that migrate authorized Campaign KV visual language to new products or multi-SKU campaign assets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce, brand, advertising, agency operations, and content teams use this skill to turn product materials, audience, channel, style-reference, and output requirements into actionable IMIVA visual migration tasks. It supports authorized Campaign KV style migration, task submission guidance, task lookup, and result review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs a mutable remote npm package through npx.

Mitigation: Review or change the helper and MCP configuration to pin the package version before using it with business assets or billable account credits.

Risk: The MCP token may be able to invoke any MCP tool available to that account.

Mitigation: Use a narrowly scoped, revocable MCP token and restrict callable MCP tools before deployment.

Risk: Implicit invocation can submit MCP operations before the user has fully reviewed cost or asset choices.

Mitigation: Disable implicit invocation or require explicit confirmation of generation count, model, resolution, and credit budget before task creation.

## Reference(s):

- [IMIVA AI电商专家 homepage](https://imiva.ecpro.com/)
- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/ai-ecommerce-expert-campaign-kv-style-migration)
- [MCP configuration example](artifact/references/mcp-config.example.json)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, JSON, API calls]

**Output Format:** [Markdown guidance with shell commands and JSON MCP arguments]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces IMIVA MCP task parameters and workflow guidance; task results are returned by the connected MCP service.]

## Skill Version(s):

1.0.0 (source: server release and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
