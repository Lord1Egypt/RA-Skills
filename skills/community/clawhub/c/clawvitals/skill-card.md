## Description:

Security vitals checker for OpenClaw that scans an installation, scores the setup, and reports prioritized fixes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bk-cm](https://clawhub.ai/user/bk-cm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators of self-hosted OpenClaw installations use this skill to run point-in-time security and health checks, receive a scored posture summary, and review concrete remediation guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads local OpenClaw security and health posture to generate its report.

Mitigation: Run it only in environments where the agent may inspect OpenClaw posture, and follow the skill's field-extraction rules so secrets and raw command output are not displayed.

Risk: The OpenClaw update-status command may contact the OpenClaw update registry.

Mitigation: Skip the update-status step when a fully offline scan is required, and mark dependent version controls as N/A.

Risk: The README install example uses an unpinned npx clawhub command.

Mitigation: Use a pinned and trusted ClawHub installer path in sensitive environments.

Risk: Scan output includes ClawVitals plugin and dashboard promotion.

Mitigation: Treat promotional text as separate from security findings and rely on directly supported control results for decisions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/bk-cm/skills/clawvitals)
- [ClawVitals Website](https://clawvitals.io)
- [ClawVitals Docs](https://clawvitals.io/docs)
- [ClawVitals Controls](https://clawvitals.io/docs/controls)
- [OpenClaw](https://openclaw.ai)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown report with tables, control results, and remediation text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill reports only supported control findings and marks unavailable checks as N/A.]

## Skill Version(s):

1.4.8 (source: release evidence and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
