## Description: <br>
Installs Gate MCP servers and Gate skills for Cursor, with support for selected MCP targets and preserving existing MCP configuration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gate-exchange](https://clawhub.ai/user/gate-exchange) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Cursor users use this skill to configure Gate MCP servers and install Gate skills for trading or research workflows in Cursor. It helps set up local and remote Gate MCP entries, skill files, and post-install restart or authentication guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The installer can make broad lasting changes to Cursor MCP configuration and skills directories. <br>
Mitigation: Back up ~/.cursor/mcp.json and ~/.cursor/skills before installation, install only the MCPs needed, and verify the resulting entries after the script runs. <br>
Risk: The installer can fetch unpinned remote Gate skills. <br>
Mitigation: Review the installed skill files before using them in sensitive workflows, or use --no-skills when only MCP configuration is required. <br>
Risk: Trading-enabled Gate API credentials may be stored in local Cursor configuration. <br>
Mitigation: Avoid entering trading-enabled API keys unless needed, limit permissions on any keys used, and mask secrets in user-visible output. <br>


## Reference(s): <br>
- [Gate Cursor Installer MCP Specification](artifact/references/mcp.md) <br>
- [Gate MCP](https://github.com/gate/gate-mcp) <br>
- [Gate Skills](https://github.com/gate/gate-skills) <br>
- [ClawHub skill page](https://clawhub.ai/gate-exchange/gate-mcp-cursor-installer) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON configuration details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce installer command options, MCP configuration guidance, and restart or authentication next steps.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata; artifact frontmatter version 2026.3.25-2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
