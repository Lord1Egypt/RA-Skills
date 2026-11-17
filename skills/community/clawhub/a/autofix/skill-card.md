## Description:

Diagnoses and helps repair OpenClaw issues through structured checks, documentation search, validation, reports, optional dashboarding, and Gateway monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mikewongonline](https://clawhub.ai/user/mikewongonline)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to diagnose Gateway, CLI, configuration, credential, and runtime issues, generate reports or dashboards, and apply or review repair steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional watchdog can persist as a background monitor and may be configured to launch on login.

Mitigation: Keep the watchdog disabled unless continuous monitoring is needed, and avoid using --install autostart until the behavior has been reviewed.

Risk: Diagnostics and alerts can include local configuration, logs, sessions, and credential-derived status data sent through Feishu or WebChat.

Mitigation: Use the skill only with reviewed alert channels, avoid sensitive logs unless alerts are redacted, and prefer offline or explicit provider-bound credential checks.

Risk: Automatic repairs may affect OpenClaw gateway processes, local sessions, or configuration with weak scoping controls.

Mitigation: Review repair scope before execution, keep rollback or baseline comparison available, and reserve automatic repair for clearly low-risk actions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mikewongonline/skills/autofix)
- [README.md](artifact/README.md)
- [INSTALL.md](artifact/INSTALL.md)
- [SKILL.md](artifact/SKILL.md)
- [CHANGES_v6.1.md](artifact/docs/reports/CHANGES_v6.1.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and optional JSON, HTML dashboard, or diagnostic report artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May recommend or invoke OpenClaw-specific diagnostic, validation, watchdog, and repair scripts.]

## Skill Version(s):

6.1.0 (source: server release, created 2026-05-22)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
