## Description:

Clawdbot Security Check helps an agent audit Clawdbot configuration across security domains, identify hardening opportunities, and recommend remediations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thesethrose](https://clawhub.ai/user/thesethrose)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to review Clawdbot deployments for risky configuration, exposed interfaces, weak access controls, credential handling issues, and missing hardening controls. It is intended to produce security findings and remediation guidance for an agent-assisted audit.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill describes itself as read-only while documenting --fix behavior that can change configuration.

Mitigation: Review or remove the --fix workflow before installation, or disclose write access and require explicit operator approval for any remediation step.

Risk: Audit commands may print full configuration files or environment-derived values that could contain secrets.

Mitigation: Use redacted, allowlisted parsing of non-secret settings and avoid storing raw config output in transcripts or logs.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/thesethrose/skills/clawdbot-security-check)
- [ClawdBot gateway security documentation](https://docs.clawd.bot/gateway/security)
- [Daniel Miessler security hardening framework reference](https://x.com/DanielMiessler/status/2015865548714975475)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Security audit reports may include severity-ranked findings, pass/fail check summaries, and remediation steps.]

## Skill Version(s):

2.2.2 (source: ClawHub release evidence and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
