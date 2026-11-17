## Description:

Clawpilot helps AI agents install, configure, secure, troubleshoot, and deploy OpenClaw self-hosted chat-to-agent gateways, with bundled reference material and local inspection scripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jason513597](https://clawhub.ai/user/jason513597)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use Clawpilot to guide OpenClaw installation, channel setup, secure configuration, audits, transcript checks, multi-agent routing, and cloud deployment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A bundled audit script can print live secrets from an OpenClaw config into terminal output or agent logs.

Mitigation: Review scripts before installation, avoid running security_audit.sh against configs with live inline tokens, prefer environment variables, and rotate any exposed credentials.

Risk: Latest-style install commands can pull unreviewed package versions.

Mitigation: Pin install commands to reviewed versions before use in production or trusted environments.

## Reference(s):

- [Clawpilot on ClawHub](https://clawhub.ai/jason513597/skills/clawpilot)
- [OpenClaw documentation index](https://docs.openclaw.ai/llms.txt)
- [OpenClaw](https://openclaw.ai)
- [OpenClaw releases](https://github.com/openclaw/openclaw/releases)
- [Configuration Reference](references/configuration.md)
- [Security Hardening](references/security.md)
- [Cloud Deployment](references/cloud-deployment.md)
- [Multi-Agent and Routing](references/multi-agent.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with code blocks and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes best-effort local inspection scripts; review outputs before acting on security recommendations.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
