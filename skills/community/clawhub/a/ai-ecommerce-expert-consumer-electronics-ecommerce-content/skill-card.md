## Description:

AI电商专家｜3C 数码电商图片视频 helps 3C consumer electronics ecommerce teams use IMIVA MCP workflows to generate product detail pages, main images, seeding content, and product videos from verified product materials.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External 3C consumer electronics brands, merchants, operators, designers, and marketing teams use this skill to structure IMIVA MCP requests for ecommerce images, detail pages, KOC or UGC seeding content, and product videos. It guides users through material checks, channel and budget confirmation, task submission, task lookup, and output review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release evidence flags the skill as requiring review because it runs an unpinned npm package with an MCP token and inherited local environment.

Mitigation: Use a narrowly scoped IMIVA token, avoid launching it from a shell containing unrelated secrets, and prefer a pinned package version or controlled MCP configuration before billable workflows.

Risk: Image and video generation tasks may consume platform credits, and repeated task creation can cause duplicate charges.

Mitigation: Check available credits first, use dry-run estimates for video workflows, confirm the budget with the user, preserve task IDs, and query existing tasks before resubmitting.

Risk: Generated ecommerce content can misstate product attributes, misuse protected third-party assets, or create misleading promotional claims.

Mitigation: Use only user-provided or confirmed product facts, verify channel-specific text and claims before publication, and require authorization before referencing competitor or viral creative materials.

## Reference(s):

- [IMIVA homepage](https://imiva.ecpro.com/)
- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/ai-ecommerce-expert-consumer-electronics-ecommerce-content)
- [MCP configuration example](references/mcp-config.example.json)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration, JSON]

**Output Format:** [Markdown guidance with shell command examples, MCP configuration snippets, and JSON tool arguments]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce IMIVA MCP task parameters and task IDs for follow-up queries when the external service is executed.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
