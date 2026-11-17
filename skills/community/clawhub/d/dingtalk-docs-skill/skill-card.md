## Description:

A DingTalk Docs agent skill for reading, creating, updating, exporting, downloading, and managing DingTalk cloud documents through the official dingtalk-doc MCP server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cpsean](https://clawhub.ai/user/cpsean)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent users use this skill to connect an MCP-capable agent to DingTalk Docs, push local Markdown or files into a knowledge base, sync or export cloud documents, and manage folders and permissions with confirmation before writes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A personal API-key URL may be persisted in agent configuration or exposed in chat or logs.

Mitigation: Use only an official HTTPS DingTalk MCP URL, prefer project-local configuration, do not commit or share MCP config files containing the URL, and rotate the URL if it was pasted or logged.

Risk: MCP traffic could be directed to a non-DingTalk endpoint if endpoint checks are bypassed.

Mitigation: Approve only official DingTalk domains for MCP URLs and reject non-DingTalk endpoints before registering the server.

Risk: Cloud document reads, downloads, exports, and uploads move data between the local environment and DingTalk and can create portable copies or temporary signed links.

Mitigation: Confirm write and transfer operations with the user, read only the documents needed for the task, disclose where data will go, and avoid long-term sharing of temporary download links.

## Reference(s):

- [DingTalk Docs MCP tool reference](references/mcp-tools.md)
- [DingTalk AI Hub MCP page](https://aihub.dingtalk.com/#/detail?mcpId=9629&detailType=marketMcpDetail)
- [DingTalk Developer guide](https://open.dingtalk.com/document/dingstart/dingtalk-developer)
- [DingTalk Docs](https://alidocs.dingtalk.com)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose MCP tool calls and file-transfer workflows; write operations require user confirmation.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
