## Description: <br>
Install, configure, authenticate, or verify a BasicOps MCP connection in an MCP-capable environment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hjhlarsen](https://clawhub.ai/user/hjhlarsen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to register, authenticate, and verify a BasicOps MCP server in MCP-capable clients before handing off to an operator skill for BasicOps work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup flow may require an agent to handle a BasicOps API key or bearer token. <br>
Mitigation: Use scoped or revocable credentials when possible, prefer secret storage or environment variables, and avoid pasting live tokens into chat unless necessary. <br>
Risk: The setup flow may modify local MCP client configuration. <br>
Mitigation: Use the client's native MCP management flow when available and verify the connection with a low-risk read or probe after configuration. <br>


## Reference(s): <br>
- [BasicOps MCP setup flow](references/setup-flow.md) <br>
- [BasicOps MCP client patterns](references/client-patterns.md) <br>
- [BasicOps MCP verification](references/verification.md) <br>
- [BasicOps MCP troubleshooting](references/troubleshooting.md) <br>
- [BasicOps MCP endpoint](https://app.basicops.com/mcp) <br>
- [ClawHub skill page](https://clawhub.ai/hjhlarsen/basicops-mcp-setup) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown] <br>
**Output Format:** [Markdown with inline shell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include client-specific MCP configuration steps, verification checks, and restart or reload instructions.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
