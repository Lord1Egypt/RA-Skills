## Description:

AI电商专家｜快手电商 图片视频全内容 helps ecommerce merchants and operations teams prepare IMIVA MCP requests for Kuaishou product images, detail-page content, seeding assets, advertising creatives, and product videos.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce merchants, brand teams, designers, advertisers, and agency operators use this skill to turn product materials, verified selling points, channel goals, and format requirements into IMIVA MCP calls for Kuaishou ecommerce content production.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release was flagged as suspicious because it auto-runs a mutable npm MCP package while passing local environment variables and token-bearing configuration.

Mitigation: Pin and review the npm package version, run it in a restricted environment, clear unrelated shell secrets, and use a dedicated low-scope MCP token.

Risk: Generation tasks can be billable when submitted to the IMIVA service.

Mitigation: Use dry-run or credit-check workflows before creating tasks, set user-confirmed credit limits, and retain task IDs to avoid duplicate submissions.

## Reference(s):

- [IMIVA AI Ecommerce Expert](https://imiva.ecpro.com/)
- [ClawHub Skill Page](https://clawhub.ai/wubin1836/skills/ai-ecommerce-expert-kuaishou-ecommerce-content)
- [ClawHub Publisher Profile](https://clawhub.ai/user/wubin1836)
- [MCP configuration example](references/mcp-config.example.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON configuration examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces IMIVA MCP task parameters, budget-check guidance, task-query commands, and content review criteria; it does not directly return generated media.]

## Skill Version(s):

1.0.0 (source: frontmatter, ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
