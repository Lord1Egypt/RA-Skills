## Description: <br>
Provides 18 OpenClaw tools for task management, skill loading, code navigation, config management, and MCP client interactions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[v4leileiv4](https://clawhub.ai/user/v4leileiv4) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers using OpenClaw use this plugin to give an agent utility tools for lightweight task tracking, skill discovery, code navigation stubs, configuration prompts, and calls to trusted MCP HTTP servers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-directed MCP HTTP calls can send prompts, secrets, workspace data, or requests to localhost or internal endpoints. <br>
Mitigation: Use only trusted MCP servers, avoid internal admin or metadata endpoints unless intentional, and do not pass sensitive data to remote MCP tools unless sharing is intended. <br>
Risk: Some code navigation and configuration tools return stub or guidance responses rather than performing live LSP or configuration operations. <br>
Mitigation: Review tool responses before acting on them and use the actual OpenClaw gateway, configuration commands, or LSP integration for authoritative changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/v4leileiv4/customtools) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, configuration, guidance] <br>
**Output Format:** [OpenClaw tool responses, usually plain text with JSON for structured task and configuration data.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [MCP tool output depends on the contacted server; code navigation and configuration tools may return guidance or stub responses.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
