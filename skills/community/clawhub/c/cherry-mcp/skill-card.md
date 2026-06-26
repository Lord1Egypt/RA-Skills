## Description: <br>
HTTP bridge that keeps MCP servers alive and exposes them via REST for OpenClaw agents that need MCP tools without native MCP support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[BitBrujo](https://clawhub.ai/user/BitBrujo) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to keep configured MCP servers running as local child processes and expose their tools through REST endpoints for agents without native MCP support. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local bridge can expose powerful configured MCP tools through an unauthenticated localhost HTTP API. <br>
Mitigation: Keep the service bound to 127.0.0.1, configure only trusted MCP server commands, and add authentication or firewall controls before using high-privilege tools. <br>
Risk: API keys and other secrets can be stored or printed in plaintext through config.json and show-config output. <br>
Mitigation: Avoid storing secrets with set-env when possible, protect config.json, and do not share show-config output. <br>
Risk: Persistent MCP server processes can continue invoking configured tools while the bridge is running. <br>
Mitigation: Review configured server commands before startup, enable audit logging for sensitive use, and remove unused servers from the configuration. <br>


## Reference(s): <br>
- [Cherry Mcp on ClawHub](https://clawhub.ai/BitBrujo/cherry-mcp) <br>
- [BitBrujo publisher profile](https://clawhub.ai/user/BitBrujo) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell command, JSON configuration, and REST API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes local bridge setup guidance and security notes for configured MCP tools.] <br>

## Skill Version(s): <br>
1.0.3 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
