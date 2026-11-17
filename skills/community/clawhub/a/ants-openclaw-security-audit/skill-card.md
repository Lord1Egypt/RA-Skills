## Description:

Audits local OpenClaw security configuration and runtime exposure, covering proxy, sandbox, Docker ports, gateway, file permissions, workspace symlinks, listening ports, and overall local security posture.

This skill is ready for commercial/non-commercial use.

## Publisher:

[asantssec](https://clawhub.ai/user/asantssec)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to inspect local OpenClaw deployments, sandbox environments, and development machines for configuration, network exposure, permissions, proxy, gateway, and symlink risks. It helps produce a prioritized audit report with evidence, risk levels, limitations, and remediation guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads local OpenClaw-related configuration paths and reports host state, which may reveal sensitive local details.

Mitigation: Run it only in environments where local audit access is acceptable, and review reports before sharing them outside the trusted team.

Risk: Proxy audit output may include live credentials or credential-bearing URLs.

Mitigation: Redact tokens, gateway URLs, and other credentials from transcripts, logs, and audit reports before distribution.

Risk: The workspace symlink check has a reliability weakness and should not be treated as definitive.

Mitigation: Confirm symlink containment findings manually or with an independent path-containment check before making security decisions.

## Reference(s):

- [OpenClaw Security Audit on ClawHub](https://clawhub.ai/asantssec/skills/ants-openclaw-security-audit)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown audit report with JSON tool outputs and remediation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local paths, port bindings, file permissions, configuration snippets, and proxy findings that should be reviewed before sharing.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
