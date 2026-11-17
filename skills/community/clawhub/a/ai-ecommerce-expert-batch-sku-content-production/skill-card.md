## Description:

AI电商专家｜批量 SKU 内容生产 helps ecommerce teams prepare IMIVA MCP workflows for batch product visual migration across multiple SKUs using authorized product and reference assets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce operators, brand teams, agencies, and supply-chain teams use this skill to turn product assets, reference visuals, channel requirements, and budget choices into IMIVA MCP task parameters for batch SKU image and video content production.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs mutable third-party MCP code and requires environment access for IMIVA credentials.

Mitigation: Install only from trusted IMIVA sources, prefer a pinned package version, and run it in a low-privilege environment containing only required MCP_TOKEN and API_URL variables.

Risk: Authorized product assets and local business files may be sent to the IMIVA service during task creation.

Mitigation: Use only assets the user is authorized to process and keep the working environment limited to files needed for the current task.

Risk: Image or video generation tasks may consume paid credits.

Mitigation: Require explicit user confirmation of model, quantity, specifications, and budget before creating paid tasks, and reuse saved task IDs for status checks.

Risk: Broad invocation and tool scope may trigger the skill in contexts where ecommerce asset processing was not intended.

Mitigation: Confirm that the user is intentionally requesting IMIVA ecommerce content generation before invoking MCP tools or processing local files.

## Reference(s):

- [IMIVA AI电商专家 homepage](https://imiva.ecpro.com/)
- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/ai-ecommerce-expert-batch-sku-content-production)
- [Example IMIVA MCP configuration](artifact/references/mcp-config.example.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON arguments, shell command examples, and MCP configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include MCP task IDs, model and specification choices, budget confirmation steps, and result review guidance.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
