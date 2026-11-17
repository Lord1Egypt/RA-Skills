## Description:

AI电商专家｜Etsy 图片视频全内容 helps Etsy merchants, operators, designers, ad teams, and agency teams prepare ecommerce product images, detail-page content, and video assets through the IMIVA MCP workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce sellers and content operations teams use this skill to turn product materials, channel goals, audience details, and budget constraints into IMIVA MCP task calls for Etsy-oriented listing images, marketing visuals, detail content, and video generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs an unpinned remote npm MCP package with a sensitive MCP token and the local environment.

Mitigation: Review before installing, use a clean low-privilege environment with no unrelated secrets, and prefer a pinned and reviewed version of the npm MCP package.

Risk: Image and video generation tasks may spend account credits when created.

Mitigation: Confirm expected credit spend, generation count, model, and specifications before creating tasks.

## Reference(s):

- [IMIVA homepage](https://imiva.ecpro.com/)
- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/ai-ecommerce-expert-etsy-ecommerce-content)
- [MCP configuration example](references/mcp-config.example.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline JSON and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose MCP tool calls and generation parameters that require user confirmation before spending credits.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
