## Description: <br>
Guidance for installing and using Fli correctly as a CLI and MCP server for flight search workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[punitarani](https://clawhub.ai/user/punitarani) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and agent users use this skill to install Fli, run flight-search commands, configure the STDIO MCP server for assistants, and troubleshoot common setup issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional HTTP MCP mode can expose a local service if configured too broadly. <br>
Mitigation: Prefer the STDIO MCP server for local assistant integration; use HTTP mode only when needed and keep it bound to localhost. <br>
Risk: Assistant configuration changes can break tool discovery if command paths or JSON are incorrect. <br>
Mitigation: Review Claude Desktop configuration changes before applying them and verify `fli-mcp --help` works in a terminal. <br>


## Reference(s): <br>
- [Fli Introduction](https://punitarani-fli.mintlify.app/introduction) <br>
- [Fli Installation](https://punitarani-fli.mintlify.app/installation) <br>
- [Fli MCP Setup](https://punitarani-fli.mintlify.app/mcp/setup) <br>
- [Fli Docs Index](https://punitarani-fli.mintlify.app/llms.txt) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with bash and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Focuses on CLI and MCP setup guidance; does not run flight searches by itself.] <br>

## Skill Version(s): <br>
0.8.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
