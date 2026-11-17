## Description:

AI电商专家｜达人 UGC 商品图 helps ecommerce, brand, KOC/KOL, and social commerce teams prepare IMIVA MCP requests for UGC-style product image workflows, including product facts, source assets, task submission, task lookup, and result review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce operators, brand content teams, merchants, and social media teams use this skill to turn product assets and channel goals into IMIVA MCP calls for UGC-style product collage generation. The workflow emphasizes budget confirmation, factual product claims, task tracking, and channel-specific result review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill launches a mutable external npm package with an IMIVA token and access to the caller's environment.

Mitigation: Use a dedicated IMIVA token, run the MCP server in a sandboxed environment, avoid unrelated secrets in that environment, and prefer a pinned or audited package version where possible.

Risk: Image or video generation tasks can consume IMIVA credits.

Mitigation: Confirm model, resolution, quantity, and maximum budget with the user before task creation; retain task IDs and query existing tasks instead of resubmitting after failures.

Risk: Generated ecommerce content can contain inaccurate product details or unsupported marketing claims.

Mitigation: Use only user-confirmed product facts and review generated outputs for product accuracy, text, claims, layout, and channel requirements before publication.

## Reference(s):

- [IMIVA homepage](https://imiva.ecpro.com/)
- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/ai-ecommerce-expert-influencer-ugc-product-image)
- [MCP configuration example](references/mcp-config.example.json)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, API Calls]

**Output Format:** [Markdown guidance with JSON arguments, shell command examples, and IMIVA MCP task responses.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an IMIVA MCP token; task creation can consume IMIVA credits and results depend on the IMIVA MCP runtime.]

## Skill Version(s):

1.0.0 (source: server evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
