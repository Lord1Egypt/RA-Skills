## Description:

AI电商专家｜中文文字广告图 helps ecommerce design, brand marketing, advertising operations, and content teams prepare IMIVA MCP workflows for Chinese text ad posters from product assets, verified selling points, channel goals, and output specifications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce design, brand marketing, ad operations, agency, and content teams use this skill to turn product materials, verified claims, channel requirements, and budget limits into IMIVA image-refinement tasks for Chinese text advertising posters.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses an unpinned remote npm MCP package with broad inherited environment access.

Mitigation: Use a pinned and audited MCP package version when possible, provide only a narrowly scoped IMIVA token, and avoid running it in an environment that contains unrelated secrets.

Risk: Implicit invocation or task creation can submit billable IMIVA work.

Mitigation: Require explicit confirmation of model, quantity, resolution, and credit budget before creating tasks.

Risk: Generated ecommerce visuals or text can misstate product facts, prices, certifications, or claims.

Mitigation: Use only user-provided or confirmed product facts and review text, claims, layout, and channel fit before publication.

## Reference(s):

- [IMIVA homepage](https://imiva.ecpro.com/)
- [MCP configuration example](references/mcp-config.example.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls, Guidance]

**Output Format:** [Markdown with inline JSON and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include IMIVA MCP task arguments, budget-confirmation guidance, task identifiers, and review criteria for generated ecommerce assets.]

## Skill Version(s):

1.0.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
