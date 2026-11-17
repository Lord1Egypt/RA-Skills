## Description:

Guides agents through installing and configuring Agent Reach for OpenClaw, Claude Code, and similar agent environments, including channel setup and troubleshooting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pyh-pan](https://clawhub.ai/user/pyh-pan)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to set up Agent Reach content channels, verify the installation, and troubleshoot environment, package, proxy, and MCP service configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may install Agent Reach from an unpinned remote archive and modify Python and agent configuration.

Mitigation: Review commands before execution, use an isolated environment, pin and verify the Agent Reach release, and avoid npm install scripts or --break-system-packages in a primary Python environment.

Risk: Proxy passwords or Twitter cookies can be exposed if pasted directly into command-line examples.

Mitigation: Use secret storage or environment variables for credentials and avoid placing sensitive values in shell history.

Risk: Optional Exa and other MCP service configuration can connect the agent environment to third-party services.

Mitigation: Enable external services only after manual review and opt-in for the target environment.

## Reference(s):

- [Agent Reach Setup on ClawHub](https://clawhub.ai/pyh-pan/skills/agent-reach-setup)
- [Agent Reach upstream repository](https://github.com/Panniantong/agent-reach)
- [Agent Reach issues](https://github.com/Panniantong/agent-reach/issues)
- [Agent Reach documentation](https://github.com/Panniantong/agent-reach/tree/main/docs)
- [OpenClaw documentation](https://docs.openclaw.ai)
- [GitHub CLI](https://cli.github.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Code, Guidance]

**Output Format:** [Markdown with inline shell commands, configuration examples, and code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes installation, verification, troubleshooting, and optional channel configuration guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata, package.json, README.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
