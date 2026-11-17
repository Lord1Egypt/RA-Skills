## Description:

BBOT MCP服务器是一个用于管理和执行BBOT安全扫描的工具，提供模块管理、预设配置、实时监控等功能。

This skill is ready for commercial/non-commercial use.

## Publisher:

[cainingnk](https://clawhub.ai/user/cainingnk)

### License/Terms of Use:

MIT-0

## Use Case:

Security engineers and authorized operators use this skill to list BBOT modules and presets, start BBOT scans, monitor active scans, and retrieve scan results through the XiaoBenYang external API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks for and stores an external service API key.

Mitigation: Use a trusted workspace, avoid shared .env files for sensitive keys, and rotate the key if it may have been exposed.

Risk: Scan targets, scan options, and API keys are sent to the XiaoBenYang external API.

Mitigation: Use the skill only with systems you are authorized to scan and only when you trust the configured service endpoint.

Risk: The service endpoint and dependency versions may affect where data is sent and what code is installed.

Mitigation: Review the configured base URL and dependency versions before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cainingnk/skills/bbot)
- [XiaoBenYang service](https://xiaobenyang.com)
- [XiaoBenYang MCP API endpoint](https://mcp.xiaobenyang.com)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown summaries of API responses and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an XBY_APIKEY value before calling the external service.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
