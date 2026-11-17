## Description:

1688上货助手 helps an agent recognize product URLs, guide 商机助理 authorization, review upload template settings, and invoke the 商机助理 MCP service for one-click product listing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[howerlin0329](https://clawhub.ai/user/howerlin0329)

### License/Terms of Use:

MIT-0

## Use Case:

External users and commerce operators use this skill to copy or publish products into the 商机助理 platform from supplied product links. The agent can guide account-token setup, inspect current listing settings, collect missing template choices, and call the remote MCP service to create listings after confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles a 商机助理 account token and product-listing authority.

Mitigation: Use it only if you trust the publisher and 商机助理 service; keep the skill directory private and rotate the sToken if files or logs may have been exposed.

Risk: Remote MCP calls can validate product links, read account information, save upload settings, and publish products.

Mitigation: Review the displayed upload settings and confirmation prompts before allowing listing actions, and avoid overriding the configured service URL.

Risk: Temporary parameter or session files may contain request details.

Mitigation: Delete temporary files after use, especially on shared machines.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/howerlin0329/skills/1688shanghuozhushou)
- [商机助理 platform](https://sjzl.fjdaze.com/)
- [商机助理 authorization page](https://sjzl.fjdaze.com/v2/#/)
- [Configured MCP service endpoint](https://api.fjdaze.cn/skillmanager/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls, Guidance]

**Output Format:** [Markdown text with command examples and JSON request parameters]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update skill-config.json with an sToken and create temporary MCP parameter or session files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
