## Description:

AI电商专家｜电商信息图套装 helps ecommerce creative, operations, brand visual, and advertising teams prepare IMIVA MCP requests for product infographic sets such as size, material, structure, comparison, and usage-step images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

Ecommerce content teams use this skill to turn product assets, verified selling points, target channel requirements, and budget choices into executable IMIVA MCP task parameters for Chinese ecommerce infographic production. It is intended for workflows such as product information graphics, size charts, structure diagrams, parameter graphics, usage steps, comparison images, and task follow-up.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs a mutable npm MCP package with credentials.

Mitigation: Use a dedicated, revocable IMIVA token with minimal permissions and prefer a pinned, reviewed package version or restricted MCP configuration.

Risk: The MCP integration exposes broader tool-calling authority than the advertised infographic workflow needs.

Mitigation: Review available tools before use and restrict the MCP configuration to the minimum tools required for the workflow.

Risk: Paid generation tasks or local product assets may be submitted to the IMIVA service.

Mitigation: Confirm costs, task parameters, and asset sharing with the user before submitting generation tasks.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/ai-ecommerce-expert-ecommerce-infographic-set)
- [IMIVA homepage](https://imiva.ecpro.com/)
- [MCP configuration example](artifact/references/mcp-config.example.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON configuration and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May prepare IMIVA MCP tool-call arguments for ecommerce content generation and task querying.]

## Skill Version(s):

1.0.0 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
