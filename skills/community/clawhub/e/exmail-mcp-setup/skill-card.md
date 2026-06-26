## Description: <br>
Set up a Tencent enterprise email MCP connector for WorkBuddy with tools to read, search, inspect, and send Exmail messages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wildbyteai](https://clawhub.ai/user/wildbyteai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and WorkBuddy users use this skill to install and configure an MCP server that connects Tencent Exmail accounts for mailbox search, message retrieval, and optional email sending. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The connector needs persistent access to the user's Exmail account credentials. <br>
Mitigation: Use a client-specific auth code rather than the login password, store it securely, and rotate or revoke it when access is no longer needed. <br>
Risk: The bundled server exposes email-sending capability as the configured account. <br>
Mitigation: Remove or disable the send_email tool unless sending mail through the agent is explicitly required. <br>
Risk: TLS certificate verification is disabled in both the setup guidance and the reference server. <br>
Mitigation: Prefer a version that keeps TLS certificate verification enabled and only use disabled verification after an explicit security review. <br>


## Reference(s): <br>
- [Reference MCP server implementation](references/index.js) <br>
- [ClawHub skill page](https://clawhub.ai/wildbyteai/exmail-mcp-setup) <br>
- [Publisher profile](https://clawhub.ai/user/wildbyteai) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash, JSON, and JavaScript code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces setup steps for a local WorkBuddy MCP server and JSON responses from Exmail tools.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
