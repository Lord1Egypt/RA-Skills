## Description: <br>
BBOT MCP服务器是一个用于管理和执行BBOT安全扫描的工具，提供模块管理、预设配置、实时监控等功能。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cainingnk](https://clawhub.ai/user/cainingnk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Security teams, developers, and authorized operators use this skill to list BBOT modules and presets, start scans against permitted targets, monitor scan status, wait for completion, and retrieve scan results through an external XiaoBenYang MCP service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can initiate security scans and may send targets and scan results to an external service. <br>
Mitigation: Use it only for assets the user owns or is authorized to test, and disclose the external service path before submitting sensitive targets. <br>
Risk: The skill stores the XiaoBenYang API key in a local .env file. <br>
Mitigation: Prefer short-lived or scoped API keys, protect the workspace, and rotate the key if the workspace is shared or exposed. <br>
Risk: Server security evidence flags inconsistent BBOT, Gaokao, and XiaoBenYang documentation and configuration. <br>
Mitigation: Review the publisher's documentation and resolved configuration before routine use, especially before relying on scan results. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cainingnk/skills/bbot) <br>
- [Publisher profile](https://clawhub.ai/user/cainingnk) <br>
- [XiaoBenYang service](https://xiaobenyang.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, configuration, guidance] <br>
**Output Format:** [Markdown summaries of JSON API responses and status messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an API key and authorized scan targets; tool calls return raw JSON, success status, and message fields.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
