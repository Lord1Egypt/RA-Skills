## Description:

AI电商专家｜爆款主图复刻与改造 helps ecommerce creative, photography, operations, brand visual, and advertising teams turn authorized reference main images and product assets into original IMIVA visual-migration tasks for product listings and campaigns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce teams use this skill to prepare IMIVA MCP visual-migration tasks that adapt the composition, lighting, and visual rhythm of authorized high-performing main images to their own product assets. It supports product listing, marketplace campaign, social commerce, KOC/UGC, and product image or video production workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill launches an unpinned remote IMIVA MCP npm package and passes environment variables into that process.

Mitigation: Use a dedicated low-privilege IMIVA token, pin a reviewed package version when deploying, and run with a minimal environment allowlist.

Risk: Creating IMIVA visual-migration tasks can consume credits or submit billable work.

Mitigation: Confirm the model, quantity, resolution, and credit limits with the user before task creation.

Risk: Reference or competitor imagery may be unauthorized or may include protected marks, people, or product claims.

Mitigation: Use only authorized source assets, migrate generic layout and lighting rather than protected expression, and review outputs before publication.

## Reference(s):

- [IMIVA AI ecommerce expert homepage](https://imiva.ecpro.com/)
- [ClawHub skill listing](https://clawhub.ai/wubin1836/skills/ai-ecommerce-expert-bestseller-main-image)
- [MCP configuration example](references/mcp-config.example.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON MCP arguments, shell command examples, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May prepare IMIVA visual-migration task parameters and task-query commands; task creation should wait for user confirmation of model, quantity, resolution, and credit limits.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
