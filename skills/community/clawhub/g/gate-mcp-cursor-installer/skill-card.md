## Description:

Gate MCP and Gate skills installer for Cursor.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gate-exchange](https://clawhub.ai/user/gate-exchange)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Cursor users use this skill to install selected Gate MCP servers, optionally install the Gate skills bundle, and receive restart and authentication guidance for Gate trading or research tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer makes persistent changes to Cursor MCP configuration and can install all Gate skills by default.

Mitigation: Review the selected MCP list before running the installer, choose only required MCPs, and use --no-skills when the full skills bundle is not needed.

Risk: Gate API credentials may be stored in Cursor configuration for local CEX use.

Mitigation: Use limited, IP-restricted keys where possible, avoid high-privilege trading keys, and remove credentials from configuration when no longer needed.

Risk: The installer pulls mutable remote code or instructions during setup.

Mitigation: Pin or review the exact gate-mcp version and gate-skills commit before running the installer.

## Reference(s):

- [Gate Cursor Installer MCP Specification](references/mcp.md)
- [ClawHub Skill Page](https://clawhub.ai/gate-exchange/skills/gate-mcp-cursor-installer)
- [Gate MCP Documentation](https://github.com/gate/gate-mcp)
- [Gate Skills Bundle](https://github.com/gate/gate-skills)
- [Gate API Key Management](https://www.gate.com/myaccount/profile/api-key/manage)
- [Gate Web3](https://web3.gate.com/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with bash commands, JSON configuration guidance, and installation status notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update Cursor MCP configuration and install Gate skill directories when the installer is executed.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact frontmatter version 2026.3.25-2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
