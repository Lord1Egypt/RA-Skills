## Description: <br>
Helps agents operate DingTalk Docs through the official DingTalk Docs MCP Server, including document creation, reading, updates, search, export, permission management, and setup guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cpsean](https://clawhub.ai/user/cpsean) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and knowledge workers use this skill to connect an MCP-capable agent to DingTalk Docs and manage cloud documents from natural-language requests. It is intended for DingTalk Docs workflows such as pushing local markdown, pulling cloud content, editing documents, exporting files, and managing document nodes and permissions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can modify DingTalk Docs content, files, nodes, exports, and permissions using the user's account permissions. <br>
Mitigation: Require explicit user confirmation before write, delete, export, upload, move, copy, rename, or permission-management actions, and summarize the target and change before execution. <br>
Risk: The DingTalk MCP StreamableHttp URL contains sensitive credentials. <br>
Mitigation: Treat the URL as a credential, avoid repeating it after configuration, and keep local MCP configuration files out of version control. <br>
Risk: Overwrite or delete operations may affect the wrong document if the target is ambiguous. <br>
Mitigation: Resolve and confirm document titles, node locations, and operation modes before destructive or replacing changes; deletion should be described as moving the item to the recycle bin. <br>


## Reference(s): <br>
- [Dingtalk Docs Skill on ClawHub](https://clawhub.ai/cpsean/dingtalk-docs-skill) <br>
- [DingTalk AI Hub MCP Page](https://aihub.dingtalk.com/#/detail?mcpId=9629&detailType=marketMcpDetail) <br>
- [DingTalk Developer Getting Started](https://open.dingtalk.com/document/dingstart/dingtalk-developer) <br>
- [MCP Tools Reference](artifact/references/mcp-tools.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown responses with inline shell commands, configuration snippets, and DingTalk document links when available] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide the agent to call DingTalk Docs MCP tools and to request user confirmation before write, delete, export, upload, or permission changes.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
