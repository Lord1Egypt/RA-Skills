## Description: <br>
Control and use an MCP Toolkit running in Docker for setup, status checks, server and tool management, environment configuration, and local MCP tool invocation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pcauhi](https://clawhub.ai/user/pcauhi) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to manage Docker Desktop MCP Toolkit servers and tools, run preflight checks, and invoke local MCP tools from OpenClaw workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can enable, disable, and invoke Docker MCP tools, which may give an agent broad access to connected systems. <br>
Mitigation: Keep enabled MCP servers minimal, use least-privilege credentials, and require explicit confirmation before configuration changes, writes, deletes, code execution, or sensitive tool calls. <br>
Risk: Exposing an MCP endpoint publicly could allow unintended remote access to local tools or credentials. <br>
Mitigation: Keep MCP endpoints local by default, bind ports to 127.0.0.1, and prefer SSH tunneling or WireGuard if remote access is required. <br>
Risk: Credential-bearing MCP tools can expose or misuse secrets when credentials are pasted into chat or shared broadly. <br>
Mitigation: Prefer Docker Desktop secrets or keychain integration, use dedicated least-privilege accounts, and rotate credentials immediately if exposed. <br>


## Reference(s): <br>
- [Security Notes](references/security.md) <br>
- [Docker MCP Toolkit Interface](references/toolkit-interface.md) <br>
- [Compose Template](references/compose-template.yml) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Tool invocation wrapper supports primitive JSON values only; nested objects and arrays require direct docker mcp commands.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
