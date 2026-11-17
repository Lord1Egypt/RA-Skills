## Description:

Helps ecommerce creative, photography, operations, brand visual, and advertising teams use IMIVA MCP to make multiple product images share one target product color while preserving consistent SKU presentation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce and brand-content teams use this skill to prepare IMIVA MCP calls for batch product image recoloring, including material review, budget checks, task submission, result queries, and channel-focused acceptance checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs a mutable external npm MCP package and sends requests with an MCP token.

Mitigation: Use a pinned and reviewed package version where possible, keep the token narrowly scoped and revocable, and provide only the minimal child-process environment required for the task.

Risk: The token may allow access to more IMIVA MCP tools than the color-change task used by this skill.

Mitigation: Create a dedicated token for this workflow, review available tools before use, and rotate or revoke the token when no longer needed.

Risk: Submitting image tasks may consume platform credits or duplicate charges if failed jobs are recreated blindly.

Mitigation: Check credits and confirm model, quantity, and resolution before submission; keep task IDs and query existing tasks before creating replacements.

## Reference(s):

- [IMIVA AI电商专家官网](https://imiva.ecpro.com/)
- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/ai-ecommerce-expert-batch-sku-color-unification)
- [MCP configuration example](references/mcp-config.example.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON configuration and inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include IMIVA MCP task parameters, task IDs, budget confirmation guidance, and result-check instructions.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
