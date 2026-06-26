## Description: <br>
One-click installer and configurator for Gate MCP (mcporter) in OpenClaw. Use when the user wants to install the mcporter CLI tool, configure the Gate MCP server connection, verify Gate MCP setup, or troubleshoot Gate MCP connectivity issues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kobin-be](https://clawhub.ai/user/kobin-be) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to install mcporter, configure the Gate MCP endpoint, verify available tools, and recover from common setup failures. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Running the installer can install or update the global mcporter npm package. <br>
Mitigation: Install only after deciding to trust the mcporter package and review the package source or registry metadata according to local policy. <br>
Risk: The installer saves a persistent Gate MCP server entry for OpenClaw. <br>
Mitigation: Remove the saved MCP configuration when Gate MCP access is no longer needed or if requests should no longer route to the external service. <br>
Risk: Setup and verification require network connectivity to the Gate MCP service. <br>
Mitigation: Verify the service endpoint and retry only on trusted networks; treat connection failures as setup blockers rather than partial success. <br>


## Reference(s): <br>
- [Gate MCP endpoint](https://api.gatemcp.ai/mcp) <br>
- [Node.js](https://nodejs.org/) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May install a global CLI and save a persistent MCP server configuration when the user runs the installer.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
