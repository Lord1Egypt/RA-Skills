## Description:

AI电商专家｜16:9 电商 TVC 广告 helps ecommerce, advertising, and brand-content teams turn product materials, confirmed claims, channel requirements, and budget constraints into IMIVA MCP workflows for Seedance 16:9 commercial video generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce operators, video editors, advertisers, brand teams, and social-commerce teams use this skill to prepare 16:9 product TVC advertisements for brand sites, conferences, YouTube, and horizontal ad placements. The skill guides users through product-fact checks, asset roles, credit estimation, task creation, task lookup, and channel-specific review before publication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill invokes a mutable npm MCP package with access to the agent runtime environment.

Mitigation: Pin the MCP package version where possible and run it with a minimal environment containing only PATH, MCP_TOKEN, and the configured API URL.

Risk: Video generation can consume paid credits when tasks are created.

Mitigation: Use dry runs to retrieve estimated credits, obtain user confirmation, set maxCredits, and keep idempotency keys and task IDs for traceability.

Risk: Generated commercial videos may contain inaccurate product claims or unauthorized reuse of reference material.

Mitigation: Use only user-provided or user-confirmed product facts, confirm authorization for reference assets, and review outputs for channel suitability before publication.

## Reference(s):

- [IMIVA homepage](https://imiva.ecpro.com/)
- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/ai-ecommerce-expert-horizontal-16-9-tvc)
- [MCP configuration example](references/mcp-config.example.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON configuration examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include MCP JSON arguments for credit checks, dry runs, task creation, and task lookup.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
