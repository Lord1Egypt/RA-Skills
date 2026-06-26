## Description: <br>
Build and publish custom MCP servers on AINative for Python FastMCP and Node.js MCP SDK workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[urbantech](https://clawhub.ai/user/urbantech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to create MCP servers, add tools, configure them for agent clients, and prepare packages for ClawHub or npm publishing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Example MCP code and configuration handle API keys. <br>
Mitigation: Store keys in environment variables or secret storage and avoid committing MCP configuration files that contain secrets. <br>
Risk: Remote memory examples can send secrets, regulated data, or sensitive prompts to AINative. <br>
Mitigation: Only send content to remote memory when retention and disclosure to AINative are intentional and acceptable for the use case. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/urbantech/ainative-mcp-builder) <br>
- [Model Context Protocol documentation](https://modelcontextprotocol.io) <br>
- [AINative API base URL](https://api.ainative.studio) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with Python, TypeScript, JSON, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only guidance; generated examples may require adaptation before use.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
