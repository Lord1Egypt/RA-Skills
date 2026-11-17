## Description:

Provides OpenClaw documentation-grounded troubleshooting and support guidance for configuration, gateway operation, channel integrations, upgrades, skills, sandboxing, model providers, webhooks, hooks, and related OpenClaw issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[isriam](https://clawhub.ai/user/isriam)

### License/Terms of Use:


## Use Case:

Developers, operators, and support agents use this skill to diagnose OpenClaw installation, gateway, configuration, channel routing, integration, and operational problems using current OpenClaw documentation and local diagnostics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may guide an agent to read OpenClaw logs and configuration files that can contain sensitive operational details.

Mitigation: Review diagnostic commands and outputs before sharing them, especially when auth, permissions, sandboxing, remote access, or tool policy are involved.

Risk: The skill may suggest configuration edits or gateway restarts that can disrupt an OpenClaw deployment.

Mitigation: Back up configuration, validate JSON, review proposed changes, restart deliberately, and check logs after changes.

## Reference(s):

- [OpenClaw Docs](https://docs.openclaw.ai)
- [OpenClaw Docs Index](https://docs.openclaw.ai/llms.txt)
- [OpenClaw Configuration Reference](https://docs.openclaw.ai/gateway/configuration-reference.md)
- [OpenClaw Gateway Troubleshooting](https://docs.openclaw.ai/gateway/troubleshooting.md)
- [OpenClaw General Troubleshooting](https://docs.openclaw.ai/help/troubleshooting.md)
- [OpenClaw FAQ](https://docs.openclaw.ai/help/faq.md)
- [OpenClaw Doctor Docs](https://docs.openclaw.ai/gateway/doctor.md)
- [OpenClaw GitHub Repository](https://github.com/openclaw/openclaw)
- [OpenClaw GitHub Issues](https://github.com/openclaw/openclaw/issues)
- [OpenClaw Releases](https://github.com/openclaw/openclaw/releases)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with inline shell commands and configuration review steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose diagnostics, log inspection, configuration validation, gateway restarts, and documentation lookups for review before execution.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
