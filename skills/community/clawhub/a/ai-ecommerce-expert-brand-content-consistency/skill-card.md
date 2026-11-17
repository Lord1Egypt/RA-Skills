## Description:

AI电商专家｜品牌电商视觉一致性 helps ecommerce and brand content teams use IMIVA MCP to migrate product visuals into a consistent brand style while preserving product facts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External brand, ecommerce, design, and multichannel content teams use this skill to prepare IMIVA visual migration tasks, confirm product facts and budget, submit image generation requests, and track results for marketplace and social commerce assets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill invokes an unpinned remote npm MCP package.

Mitigation: Review and pin a trusted version of @infimind/ecom-content-cli before installation or production use.

Risk: The MCP process receives environment variables and a token that could expose unrelated secrets if run in a broad environment.

Mitigation: Run the skill in an isolated environment with only the required MCP_TOKEN and API URL available.

Risk: Task creation may consume IMIVA credits.

Mitigation: Check available credits, confirm model, count, resolution, and budget with the user, and verify tool calls before creating tasks.

Risk: Visual migration from third-party reference assets can create IP, impersonation, or false advertising issues.

Mitigation: Use authorized references, preserve only general composition or style patterns, and validate product claims and brand elements against user-provided facts.

## Reference(s):

- [IMIVA homepage](https://imiva.ecpro.com/)
- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/ai-ecommerce-expert-brand-content-consistency)
- [MCP configuration example](artifact/references/mcp-config.example.json)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, API calls]

**Output Format:** [Markdown with JSON and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides IMIVA MCP task setup, budget checks, product fact review, task creation, and result lookup.]

## Skill Version(s):

1.0.0 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
