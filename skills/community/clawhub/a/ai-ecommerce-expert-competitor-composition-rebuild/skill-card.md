## Description:

AI电商专家｜竞品构图参考重制 helps ecommerce design, brand marketing, advertising, agency, and content teams use IMIVA MCP to rebuild product visuals from authorized competitor-composition references while preserving product facts and avoiding copied protected expression.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

Ecommerce designers, brand marketers, advertising teams, agencies, and content operators use this skill to prepare IMIVA visual migration tasks for product images, marketplace listings, detail pages, social commerce assets, and product video variants. The workflow helps users confirm source material, budget, model settings, output specifications, task IDs, and quality checks before and after MCP execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs an unpinned external npm MCP client with credentials.

Mitigation: Use a dedicated shell or sandbox with only the required IMIVA token, prefer a pinned audited package version, and avoid granting token permissions or credits beyond the intended spend.

Risk: Visual migration tasks may consume credits or misuse competitor and reference assets.

Mitigation: Confirm model, quantity, resolution, and budget before task creation, and use only authorized references while avoiding copied trademarks, identities, or protected expression.

## Reference(s):

- [IMIVA homepage](https://imiva.ecpro.com/)
- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/ai-ecommerce-expert-competitor-composition-rebuild)
- [MCP configuration example](references/mcp-config.example.json)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with bash examples, JSON configuration snippets, and MCP tool-call arguments.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include IMIVA task IDs, model and budget settings, and result-review guidance for generated ecommerce media.]

## Skill Version(s):

1.0.0 (source: server evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
