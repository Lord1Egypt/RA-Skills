## Description: <br>
AnyShare MCP Skills helps agents search, read, upload, download, share, and draft from documents in an AnyShare enterprise document-management workspace. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jerrrr](https://clawhub.ai/user/jerrrr) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and developers use this skill through OpenClaw and mcporter to work with enterprise AnyShare files: search or browse documents, parse sharing links, upload and download files, and generate outlines or full drafts from selected documents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bearer tokens can be exposed if pasted into chat, shell history, logs, or version control. <br>
Mitigation: Configure credentials through a secure local method where possible, restrict permissions on ~/.mcporter/mcporter.json, use least-privilege short-lived tokens, and rotate any token that may have been exposed. <br>
Risk: A wrong or unofficial MCP URL could route enterprise document operations to an unintended endpoint. <br>
Mitigation: Verify that the MCP URL is the organization's official AnyShare endpoint before authorizing or retrying calls. <br>
Risk: The skill can access enterprise documents according to the user's AnyShare permissions. <br>
Mitigation: Review the setup steps before installation and follow the organization's data-classification and access-control rules. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/jerrrr/anyshare-mcp-skills) <br>
- [AnyShare](https://anyshare.aishu.cn) <br>
- [Security notes](SECURITY.md) <br>
- [Troubleshooting guide](references/troubleshooting.md) <br>
- [MCP server configuration](mcp.json) <br>
- [OpenClaw skill entry configuration](openclaw.skill-entry.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON configuration and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires mcporter, an AnyShare MCP endpoint, and a bearer token configured outside normal chat where possible.] <br>

## Skill Version(s): <br>
0.2.8 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
