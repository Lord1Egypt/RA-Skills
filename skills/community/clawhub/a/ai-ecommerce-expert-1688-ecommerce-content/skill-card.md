## Description:

AI ecommerce expert for 1688 wholesale merchants that prepares IMIVA MCP workflows for product images, detail pages, seeding content, advertising assets, and product videos.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External 1688 wholesale merchants, ecommerce operators, designers, advertisers, and agency teams use this skill to turn product assets, selling points, audience, channel, budget, and output requirements into executable IMIVA MCP tasks. It supports product listing images, detail-page content, social seeding assets, ad creatives, product videos, task tracking, and result review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs an external npm MCP client with a user token and broad environment access.

Mitigation: Run it in a restricted environment with a narrowly scoped IMIVA token, a fixed trusted API endpoint, and a pinned or pre-reviewed package version before production use.

Risk: IMIVA task submission can send ecommerce assets and task parameters to an external service and may create billable tasks.

Mitigation: Confirm the user is comfortable sending the assets, check credits or estimates before submission, set spending limits where supported, and keep task IDs for follow-up instead of recreating tasks.

Risk: Generated ecommerce copy, product images, or videos could contain inaccurate product facts, misleading claims, or unauthorized use of third-party material.

Mitigation: Use only user-provided or confirmed product facts and review generated outputs for factual accuracy, rights, channel fit, and compliance before publication.

## Reference(s):

- [IMIVA homepage](https://imiva.ecpro.com/)
- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/ai-ecommerce-expert-1688-ecommerce-content)
- [MCP configuration example](references/mcp-config.example.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, API Calls, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON configuration and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include IMIVA MCP task IDs and links or paths to generated ecommerce image, detail-page, or video outputs when returned by the service.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
