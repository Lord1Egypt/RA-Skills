## Description: <br>
Dingtalk Ai Table helps an agent use mcporter to operate DingTalk AI Tables through the newer MCP schema for bases, tables, fields, records, attachments, and bulk imports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aliramw](https://clawhub.ai/user/aliramw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, operators, and developers use this skill to create, query, update, delete, and bulk-manage DingTalk AI Table bases, tables, fields, and records through a configured MCP URL. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can modify or delete DingTalk AI Table data. <br>
Mitigation: Require explicit confirmation and use a backup or test table before bulk imports, updates, schema changes, or deletions. <br>
Risk: DINGTALK_MCP_URL contains access credentials for the DingTalk MCP server. <br>
Mitigation: Treat the URL like a password and avoid exposing it in logs, shared files, or generated output. <br>
Risk: Local CSV and JSON helper scripts read user-provided files for bulk operations. <br>
Mitigation: Set OPENCLAW_WORKSPACE to a limited folder and keep import files inside that workspace. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aliramw/dingtalk-ai-table) <br>
- [Publisher profile](https://clawhub.ai/user/aliramw) <br>
- [Project documentation](https://github.com/aliramw/dingtalk-ai-table) <br>
- [Support issues](https://github.com/aliramw/dingtalk-ai-table/issues) <br>
- [DingTalk MCP configuration](https://mcp.dingtalk.com/#/detail?mcpId=9555&detailType=marketMcpDetail) <br>
- [API reference](artifact/api-reference.md) <br>
- [Error codes and troubleshooting](artifact/error-codes.md) <br>
- [Getting started](artifact/GETTING_STARTED.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Code, API Calls] <br>
**Output Format:** [Markdown guidance with bash commands, JSON payloads, and Python helper script usage] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a DingTalk MCP URL, mcporter, python3, and a workspace-limited file path for CSV or JSON imports.] <br>

## Skill Version(s): <br>
0.6.0 (source: server release evidence, SKILL.md frontmatter, package.json, CHANGELOG) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
