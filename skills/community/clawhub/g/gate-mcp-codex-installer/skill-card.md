## Description: <br>
Gate MCP and Gate skills installer for Codex. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gate-exchange](https://clawhub.ai/user/gate-exchange) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Codex users use this skill to configure selected Gate MCP servers, install the Gate skills bundle when requested, and receive restart and authorization next steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The installer makes persistent changes to Codex configuration and skill directories. <br>
Mitigation: Review the release before installing and back up ~/.codex/config.toml and ~/.codex/skills before execution. <br>
Risk: The installer can store trading credentials for Gate MCP use. <br>
Mitigation: Avoid entering trading API keys unless they are tightly scoped and required for the selected use case. <br>
Risk: Default installation can enable all Gate MCP integrations and install all Gate skills. <br>
Mitigation: Use specific --mcp selections and --no-skills when a narrower installation is sufficient. <br>
Risk: Installed Gate skills may be replaced from mutable remote content. <br>
Mitigation: Review installed skill contents after installation and before relying on them for sensitive workflows. <br>


## Reference(s): <br>
- [Gate Codex Installer MCP Specification](references/mcp.md) <br>
- [Gate MCP](https://github.com/gate/gate-mcp) <br>
- [Gate Skills](https://github.com/gate/gate-skills) <br>
- [ClawHub Release Page](https://clawhub.ai/gate-exchange/gate-mcp-codex-installer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update local Codex MCP configuration and skills directories when the installer is executed.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata; artifact frontmatter and changelog report 2026.3.25-2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
