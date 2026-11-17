## Description:

Helps ecommerce teams create mother, baby, and children's apparel product images, detail-page assets, KOC/social creative, and videos through IMIVA MCP workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce operators, brand teams, designers, and marketers use this skill to turn product materials and channel requirements into IMIVA MCP tasks for listing images, detail pages, KOC/social creative, and product videos.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on an automatically downloaded IMIVA npm package with broad environment access.

Mitigation: Install only when the IMIVA package and service are trusted, prefer pinning the package version, and limit the subprocess environment.

Risk: Product data, local media paths, and generated content requests may be sent to IMIVA.

Mitigation: Use least-privilege MCP tokens and confirm that product data and media are appropriate to share with the IMIVA service.

Risk: Media generation tasks may consume paid credits.

Mitigation: Require explicit confirmation before paid task creation and set clear task limits when the underlying tool supports them.

## Reference(s):

- [IMIVA homepage](https://imiva.ecpro.com/)
- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/ai-ecommerce-expert-mother-baby-ecommerce-content)
- [MCP config example](references/mcp-config.example.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON MCP arguments and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May prepare or execute IMIVA MCP calls that create paid media generation tasks after user confirmation.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
