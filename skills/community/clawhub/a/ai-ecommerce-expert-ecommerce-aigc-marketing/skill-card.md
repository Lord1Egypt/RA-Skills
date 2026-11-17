## Description:

AI电商专家｜电商 AIGC 营销内容 helps ecommerce marketing, advertising, content, livestream, and social commerce teams turn product inputs into IMIVA MCP-ready requests for ad images, seeding content, campaign visuals, and short-form product video.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce teams and operators use this skill to structure product media, selling points, channel requirements, budget checks, and task queries for IMIVA ecommerce content generation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill invokes a mutable npm package that receives the user's environment when run.

Mitigation: Install only after trusting the IMIVA package publisher, prefer a pinned reviewed package version, and run it from a constrained environment without unrelated secrets.

Risk: Task creation can upload business media and consume account credits.

Mitigation: Require explicit user confirmation for model, quantity, budget, and media inputs before creating paid or upload-bearing tasks.

## Reference(s):

- [IMIVA homepage](https://imiva.ecpro.com/)
- [MCP configuration example](references/mcp-config.example.json)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with JSON configuration and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces MCP task parameters and operational guidance; generated media is produced by the connected IMIVA service.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
