## Description:

Provides guidance for installing, configuring, operating, and troubleshooting OpenClaw, a self-hosted multi-channel AI agent gateway.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bengii](https://clawhub.ai/user/bengii)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to administer local OpenClaw deployments, including setup, model providers, channel management, gateway operations, security hardening, and troubleshooting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill recommends installer or update commands such as curl piped to bash or PowerShell iwr piped to iex.

Mitigation: Prefer pinned packages or signed release installers, review installer scripts before execution, and avoid running installers as root.

Risk: Troubleshooting guidance can expose secrets from files such as ~/.openclaw/.env.

Mitigation: Do not paste or print secret files into an AI session; redact values and rotate any credentials that were exposed.

Risk: Gateway administration guidance can affect remote access, authentication, tools, and subagents.

Mitigation: Keep the gateway on loopback or a private network, enable authentication, restrict tools and subagents, and use sandboxing for untrusted channels.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/bengii/skills/bengii-gemini-fix)
- [OpenClaw Skill README](artifact/README.md)
- [OpenClaw Documentation](https://docs.openclaw.ai/)
- [OpenClaw Install Documentation](https://docs.openclaw.ai/install)
- [Gateway Architecture](https://docs.openclaw.ai/concepts/architecture)
- [Security Reference](artifact/references/security.md)
- [Gateway Operations Reference](artifact/references/gateway_ops.md)
- [Installation Reference](artifact/references/install.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose commands or configuration changes that should be reviewed before execution.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
