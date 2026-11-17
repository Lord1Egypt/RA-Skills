## Description:

Installs Gate MCP server configurations and the Gate skills bundle for Codex.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gate-exchange](https://clawhub.ai/user/gate-exchange)

### License/Terms of Use:

MIT-0

## Use Case:

Codex users and developers use this skill to configure selected Gate MCP servers, optionally install the Gate skills bundle, and receive restart and authentication next steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer persistently changes Codex configuration and may fetch unpinned remote skills or packages.

Mitigation: Review the exact configuration changes before execution, prefer explicit --mcp selections, and use --no-skills unless the full remote skill bundle is intended.

Risk: Gate trading credentials can be stored in Codex configuration in plaintext.

Mitigation: Do not enter credentials unless that storage is acceptable; use least-privilege API keys, avoid withdrawal permissions, restrict keys by IP where possible, and rotate keys after exposure.

## Reference(s):

- [Gate Codex Installer MCP Specification](references/mcp.md)
- [Gate MCP](https://github.com/gate/gate-mcp)
- [Gate Skills](https://github.com/gate/gate-skills)
- [Gate Runtime Rules](https://github.com/gate/gate-skills/blob/master/skills/gate-runtime-rules.md)
- [ClawHub Skill Page](https://clawhub.ai/gate-exchange/skills/gate-mcp-codex-installer)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown status summary with shell commands and TOML configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce persistent Codex MCP configuration and skill-directory changes when the installer script is run.]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
