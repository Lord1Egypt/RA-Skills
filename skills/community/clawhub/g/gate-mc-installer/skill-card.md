## Description: <br>
One-click installer and configurator for Gate MCP (mcporter) in OpenClaw. Use when the user wants to install the mcporter CLI tool, configure a Gate MCP server connection, verify Gate MCP setup, or troubleshoot Gate MCP connectivity issues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aspiremongoai](https://clawhub.ai/user/aspiremongoai) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to install, configure, verify, update, or troubleshoot Gate MCP access through mcporter. It supports setup flows for natural-language access to Gate.io market data through the Gate MCP endpoint. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup changes the user's local toolchain by installing or updating the mcporter npm package globally. <br>
Mitigation: Install only when the user trusts the mcporter package, has Node.js and npm available, and accepts a global CLI install or update. <br>
Risk: The setup writes a home-scoped Gate MCP configuration entry. <br>
Mitigation: Review the intended Gate MCP endpoint before configuration and inspect the resulting mcporter config after installation. <br>
Risk: Verification and later use connect to an external Gate MCP service. <br>
Mitigation: Use only in environments where outbound network access to the Gate MCP endpoint is approved and expected. <br>


## Reference(s): <br>
- [Gate MCP Installer on ClawHub](https://clawhub.ai/aspiremongoai/gate-mc-installer) <br>
- [OpenClaw](https://openclaw.ai) <br>
- [Gate MCP endpoint](https://api.gatemcp.ai/mcp) <br>
- [Scenario examples](references/scenarios.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and status guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose or run commands that install mcporter globally, write a home-scoped Gate MCP configuration, and verify connectivity to the Gate MCP service.] <br>

## Skill Version(s): <br>
2026.3.4-1 (source: frontmatter, changelog, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
