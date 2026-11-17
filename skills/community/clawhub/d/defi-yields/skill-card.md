## Description:

一个为AI代理提供DeFi收益机会探索和分析的MCP服务器，支持从DefiLlama获取收益池数据并进行关键指标分析。

This skill is ready for commercial/non-commercial use.

## Publisher:

[alinklab](https://clawhub.ai/user/alinklab)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and developers use this skill to retrieve and summarize DeFi yield pool opportunities, optionally filtering by chain or project. It is intended for exploratory yield analysis and should be used with awareness that requests are routed through a third-party service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends requests through a third-party Xiaobenyang MCP service rather than acting as a simple local DefiLlama reader.

Mitigation: Review the third-party service relationship before deployment, disclose the proxy behavior to users, and restrict use to data that may be sent to that service.

Risk: The skill stores the Xiaobenyang API key in plaintext in a local .env file.

Mitigation: Use managed secret storage where available, avoid committing .env files, rotate exposed keys, and limit file access to trusted users and processes.

Risk: Unrelated Gaokao references in configuration and documentation may confuse operators about the actual service scope.

Mitigation: Confirm the configured MCP identifier and endpoint before use, and prefer a release whose documentation consistently describes the DeFi yield workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alinklab/skills/defi-yields)
- [Publisher profile](https://clawhub.ai/user/alinklab)
- [Xiaobenyang API key service](https://xiaobenyang.com)
- [Xiaobenyang MCP service](https://mcp.xiaobenyang.com)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown summaries derived from JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Xiaobenyang API key and remote service access; tool responses include raw DeFi yield pool data such as symbol, project, TVL, APY, 30-day mean APY, and predictions.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
