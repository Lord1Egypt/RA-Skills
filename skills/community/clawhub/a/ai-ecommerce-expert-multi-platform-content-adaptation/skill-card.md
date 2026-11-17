## Description:

AI电商专家｜多平台电商内容适配 helps enterprise ecommerce and operations teams prepare IMIVA MCP requests for adapting product images and videos across marketplace, social commerce, cross-border, and listing channels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce teams, brand operators, cross-border sellers, and agency users use this skill to turn verified product素材, channel goals, budget constraints, and target ratios into executable IMIVA MCP calls for image expansion, video generation, task tracking, and result review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs a mutable external npm package with broad environment access.

Mitigation: Review the package before installation, prefer a pinned reviewed version, and run it from a clean shell or container with minimal environment variables.

Risk: IMIVA MCP actions can create image or video generation tasks that may spend credits.

Mitigation: Use a narrowly scoped, revocable IMIVA token and require explicit user confirmation before creating generation tasks or approving video credit limits.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/ai-ecommerce-expert-multi-platform-content-adaptation)
- [Publisher profile](https://clawhub.ai/user/wubin1836)
- [IMIVA homepage](https://imiva.ecpro.com/)
- [MCP configuration example](references/mcp-config.example.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON and bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces MCP setup guidance, task arguments, budget-confirmation prompts, task-query commands, and quality-review checklists.]

## Skill Version(s):

1.0.0 (source: server release evidence and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
