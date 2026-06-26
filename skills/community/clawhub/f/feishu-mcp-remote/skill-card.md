## Description: <br>
Feishu MCP Remote guides agents in calling Feishu's remote MCP HTTP API for cloud document, user directory, and file access workflows with UAT or TAT authentication. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jirboy](https://clawhub.ai/user/jirboy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to connect an AI agent to Feishu cloud documents, user lookup, comments, and file retrieval through Feishu's hosted MCP endpoint. It is intended for workflows that need controlled Feishu read or write actions using user or tenant access tokens. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agents can access Feishu using UAT or TAT credentials and may read, create, update, comment on, or fetch workspace content. <br>
Mitigation: Use least-privilege tokens, keep credentials out of chat, restrict X-Lark-MCP-Allowed-Tools to the minimum required tools, and require explicit review before sensitive content operations. <br>
Risk: Write-capable Feishu tools can create documents, update documents, or add comments through the remote MCP endpoint. <br>
Mitigation: Limit write-capable tools such as create-doc, update-doc, and add-comments unless the workflow requires them, and review target document IDs and payload content before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jirboy/feishu-mcp-remote) <br>
- [Feishu MCP endpoint](https://mcp.feishu.cn/mcp) <br>
- [Lark user access token documentation](https://open.larkoffice.com/document/server-docs/api-call-guide/calling-process/get-access-token?#4d916fe0) <br>
- [Feishu tenant access token endpoint](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal) <br>
- [Lark API permission documentation](https://open.larkoffice.com/document/ukTMukTMukTM/uQjN3QjL0YzN04CN2cDN) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, configuration, API call examples] <br>
**Output Format:** [Markdown instructions with Python and JSON-RPC examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documents Feishu UAT/TAT headers, allowed-tool scoping, tool calls, and common error handling; the skill itself does not create files.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
