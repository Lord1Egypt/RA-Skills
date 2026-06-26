## Description: <br>
Connect to AutoSend email MCP server from OpenClaw using mcporter for managing email campaigns, templates, contacts, and senders via AI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shindebhau](https://clawhub.ai/user/shindebhau) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to connect OpenClaw to the AutoSend MCP server through mcporter. It supports setup, OAuth authentication, testing, and agent-assisted management of email templates, campaigns, senders, contacts, and analytics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can help an agent create, update, duplicate, or delete AutoSend email resources and generate email content. <br>
Mitigation: Use agent confirmation for create, update, duplicate, or delete actions and review generated email content before sending. <br>
Risk: AutoSend OAuth tokens are stored locally by mcporter and can grant access to email-management capabilities. <br>
Mitigation: Keep mcporter OAuth credential files private with user-only filesystem permissions and re-authenticate when credentials are invalid or expired. <br>
Risk: Installing mcporter from an untrusted source could compromise the connector workflow. <br>
Mitigation: Install mcporter from a trusted source before configuring the AutoSend MCP server. <br>


## Reference(s): <br>
- [AutoSend MCP Docs](https://docs.autosend.com/ai/mcp-server) <br>
- [AutoSend](https://autosend.com) <br>
- [mcporter GitHub](https://github.com/steipete/mcporter) <br>
- [mcporter on ClawHub](https://clawhub.ai/steipete/mcporter) <br>
- [Model Context Protocol Specification](https://modelcontextprotocol.io/) <br>
- [AutoSend MCP Skill on ClawHub](https://clawhub.ai/shindebhau/autosend-mcp-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Code] <br>
**Output Format:** [Markdown with inline bash and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires mcporter, an AutoSend account, and OAuth authentication before agent calls can manage AutoSend resources.] <br>

## Skill Version(s): <br>
0.1.3 (source: server release evidence; artifact frontmatter lists 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
