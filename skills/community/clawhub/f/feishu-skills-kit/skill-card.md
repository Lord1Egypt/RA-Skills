## Description: <br>
Complete Feishu (Lark) skills collection for Claude Code and OpenClaw agents, covering document management, messaging, spreadsheets, Bitable, interactive cards, bot bridging, cross-group memory, and leave requests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hewenqiang](https://clawhub.ai/user/hewenqiang) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this kit to connect Claude Code or OpenClaw agents to Feishu/Lark workspaces for document publishing and editing, messaging, interactive cards, spreadsheet and Bitable operations, bot bridging, memory recall, and guided leave request workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unsafe shell command construction may execute unintended commands. <br>
Mitigation: Review or disable affected helper scripts, and replace shell-string dispatch with argument-array subprocess calls or direct module calls before enabling them. <br>
Risk: Remote write scripts can send messages or modify Feishu documents, sheets, Bitable records, or workflow requests without clear user control. <br>
Mitigation: Use least-privilege Feishu app scopes, restrict approved chats and documents, and require explicit user confirmation for destructive or external-write actions. <br>
Risk: Bridge, autostart, and cross-group memory features can expose private messages across chats or accounts. <br>
Mitigation: Enable those features only for approved chats and accounts, limit retained data, and avoid uploading secrets or private files. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/hewenqiang/feishu-skills-kit) <br>
- [Release setup guide](artifact/README.md) <br>
- [MCP configuration template](artifact/mcp-config-template.json) <br>
- [Feishu Open Platform](https://open.feishu.cn/app) <br>
- [Feishu API documentation](https://open.feishu.cn/document/server-docs/api-call-guide/server-api-list) <br>
- [Feishu document editor API guide](artifact/skills/feishu-doc-editor/references/api-guide.md) <br>
- [Feishu document permission setup](artifact/skills/feishu-doc-editor/references/permission-setup.md) <br>
- [Feishu sheets API reference](artifact/skills/feishu-sheets-skill/references/api-reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with JSON configuration examples and code or shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user-provided Feishu/Lark app credentials, MCP setup, and least-privilege app permissions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
