## Description:

One-click installer and configurator for Gate MCP (mcporter) in OpenClaw that installs the CLI, configures the server connection, verifies setup, and supports troubleshooting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aspiremongoai](https://clawhub.ai/user/aspiremongoai)

### License/Terms of Use:

MIT

## Use Case:

Developers and external OpenClaw users use this skill to install, configure, verify, update, or troubleshoot Gate MCP access for natural-language Gate.io market data workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer can add or update a global mcporter npm package and write Gate MCP configuration in the user's home environment.

Mitigation: Review the installer before execution, avoid sudo or administrator privileges, and prefer a pinned, reviewed mcporter version when possible.

Risk: Gate MCP use depends on network access to https://api.gatemcp.ai/mcp.

Mitigation: Confirm endpoint connectivity during setup and treat connection failures as network or service availability issues before retrying.

## Reference(s):

- [Gate MCP Installer Scenarios and Prompt Examples](references/scenarios.md)
- [ClawHub Skill Page](https://clawhub.ai/aspiremongoai/skills/gate-mc-installer)
- [OpenClaw](https://openclaw.ai)
- [Node.js](https://nodejs.org/)
- [Gate MCP Endpoint](https://api.gatemcp.ai/mcp)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash code blocks and command output summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May prompt before reinstalling mcporter or reconfiguring an existing Gate MCP setup.]

## Skill Version(s):

2026.3.4-1 (source: SKILL.md frontmatter and CHANGELOG.md, released 2026-03-04)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
