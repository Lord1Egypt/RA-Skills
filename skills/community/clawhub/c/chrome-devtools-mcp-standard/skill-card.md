## Description:

Chrome DevTools MCP (Standard) helps agents automate and inspect local Chrome sessions for navigation, screenshots, form interaction, debugging, performance traces, Lighthouse audits, network inspection, and emulation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lac5q](https://clawhub.ai/user/lac5q)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to configure Chrome DevTools MCP and decide when to use local browser automation, debugging, audit, network, and emulation tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to give an agent broad local Chrome control.

Mitigation: Use a dedicated browser profile without sensitive sessions and only enable the MCP server for workflows that require browser control.

Risk: The artifact recommends mutable package startup through chrome-devtools-mcp@latest.

Mitigation: Pin exact package versions for repeatable deployments and review MCP startup commands before use.

Risk: The install and troubleshooting guidance includes npm, npx, sudo, package-manager, and plugin commands.

Mitigation: Review commands before running them and apply normal local software installation controls.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lac5q/skills/chrome-devtools-mcp-standard)
- [Publisher Profile](https://clawhub.ai/user/lac5q)
- [Chrome DevTools MCP GitHub Repository](https://github.com/ChromeDevTools/chrome-devtools-mcp)
- [Chrome DevTools MCP Tool Reference](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/main/docs/tool-reference.md)
- [Chrome DevTools MCP Slim Tool Reference](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/main/docs/slim-tool-reference.md)
- [Chrome DevTools MCP Troubleshooting](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/main/docs/troubleshooting.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON, YAML, and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes MCP configuration snippets, installation commands, tool-selection guidance, and troubleshooting steps.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
