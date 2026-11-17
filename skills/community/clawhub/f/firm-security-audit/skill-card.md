## Description:

Proactive security audit for OpenClaw deployments that checks SQL injection exposure, sandbox configuration, session secret persistence, rate limiting, and Matrix E2EE documentation gaps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[romainsantoli-web](https://clawhub.ai/user/romainsantoli-web)

### License/Terms of Use:

MIT

## Use Case:

Developers and deployment engineers use this skill as a security gate before OpenClaw Gateway deployment or public network exposure. It guides audits, remediation checks, and escalation for critical and high security findings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can act as a strong deployment gate with broad remediation authority.

Mitigation: Require explicit user confirmation before applying remediations, disabling services, restarting containers, or blocking a deployment.

Risk: Critical audit results may be sent to Slack automatically.

Mitigation: Confirm before sending external Slack messages and share only redacted summaries of audit findings.

Risk: The skill depends on mcp-openclaw-extensions with access to source, configuration, Compose, environment, or Slack tooling.

Mitigation: Pin and review the mcp-openclaw-extensions dependency before granting tool access.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/romainsantoli-web/skills/firm-security-audit)
- [Publisher profile](https://clawhub.ai/user/romainsantoli-web)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code, markdown]

**Output Format:** [Markdown with JSON, YAML, Nginx, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes audit sequencing, expected pass/fail conditions, remediation templates, and escalation guidance.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
