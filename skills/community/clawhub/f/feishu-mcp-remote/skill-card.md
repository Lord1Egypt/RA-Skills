## Description:

Invokes Feishu MCP remote services over HTTP so an agent can search users, retrieve files, and create, read, or update Feishu cloud documents with UAT or TAT authentication.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jirboy](https://clawhub.ai/user/jirboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to connect an AI agent to Feishu MCP tools for cloud documents, user lookup, file retrieval, and document comments through authenticated HTTP API calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use powerful Feishu UAT or TAT credentials to read or change live documents.

Mitigation: Use least-privilege token scopes, restrict X-Lark-MCP-Allowed-Tools to required tools, and confirm before creating, updating, or commenting on live documents.

Risk: Real Feishu credentials may be exposed if pasted into shared chats or logs.

Mitigation: Avoid sharing real UAT or TAT values in prompts, examples, transcripts, or logs; redact credentials when troubleshooting.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jirboy/skills/feishu-mcp-remote)
- [Feishu MCP endpoint](https://mcp.feishu.cn/mcp)
- [Get user_access_token](https://open.larkoffice.com/document/server-docs/api-call-guide/calling-process/get-access-token?#4d916fe0)
- [Tenant access token endpoint](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal)
- [Apply for API permissions](https://open.larkoffice.com/document/ukTMukTMukTM/uQjN3QjL0YzN04CN2cDN)

## Skill Output:

**Output Type(s):** [guidance, code, configuration]

**Output Format:** [Markdown with Python code blocks and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Feishu API request examples, token header configuration, tool allow-listing, and permission guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
