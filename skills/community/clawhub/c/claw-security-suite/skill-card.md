## Description:

Provides four-layer security for OpenClaw including static code scanning, logic audit, runtime protection, and periodic security patrols with automated reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kenz1117](https://clawhub.ai/user/kenz1117)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to scan OpenClaw skills before installation, audit code logic for security risks, check user input for runtime attacks, and generate periodic security patrol reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled policy claims broad installation authority that may conflict with platform or user rules.

Mitigation: Treat the policy as advisory skill documentation and keep platform, workspace, and user instructions authoritative.

Risk: Scanner containment and assurance gaps can miss issues or create unsafe assumptions in automated approval paths.

Mitigation: Run scans with low filesystem privileges, avoid untrusted archives that may contain symlinks until containment is reviewed, and require human review for install decisions.

Risk: Cloud reputation checks can contact the configured Tencent endpoint with the skill name and source when a skill_name is supplied.

Mitigation: Disable or override the cloud endpoint when outbound reputation checks are not approved for the environment.

## Reference(s):

- [Claw Security Suite on ClawHub](https://clawhub.ai/kenz1117/skills/claw-security-suite)
- [Security Policy](artifact/references/security-policy.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, guidance]

**Output Format:** [Markdown reports, text pass/fail summaries, JSON patrol reports, and Python result objects]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include advisory scan verdicts, issue counts, matched attack categories, sanitized input strings, and report file paths.]

## Skill Version(s):

1.1.0 (source: server release metadata, artifact _meta.json, CHANGELOG)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
