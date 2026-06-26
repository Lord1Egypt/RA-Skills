## Description: <br>
Create, deploy, and manage MCP (Model Context Protocol) servers using the MCPHero platform via the mcpheroctl CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[arterialist](https://clawhub.ai/user/arterialist) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to create MCPHero-hosted MCP servers, deploy tools around APIs or databases, and connect clients such as Claude Desktop or Cursor to those tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API tokens and generated bearer tokens can be exposed through shared chats, logs, or client configuration files. <br>
Mitigation: Use scoped and revocable tokens, avoid pasting real secrets into shared contexts, and protect any configuration containing Authorization headers. <br>
Risk: Generated tools or environment variables may not match the intended API or database behavior. <br>
Mitigation: Review suggested tools and environment variables before deployment and test the deployed server before giving it broader access. <br>
Risk: Server deletion is irreversible when using the documented delete command. <br>
Mitigation: Confirm the exact server identifier and intent before running destructive server management commands. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/arterialist/create-mcp-server) <br>
- [MCPHero](https://mcphero.app) <br>
- [MCPHero API base URL](https://api.mcphero.app/api) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Provides CLI workflow steps, polling patterns, deployment guidance, and client configuration examples.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
