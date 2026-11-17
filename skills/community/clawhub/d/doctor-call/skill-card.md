## Description:

Diagnose and fix OpenClaw gateway issues with optional auto-restart via systemd.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stigg86](https://clawhub.ai/user/stigg86)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to check OpenClaw gateway health, run diagnostics, repair configuration issues, and configure automatic gateway restarts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup action enables a persistent user-level systemd timer that can repair configuration and restart the OpenClaw gateway in the background.

Mitigation: Run setup only when persistent OpenClaw health management is intended; review the generated service path, timer, and removal behavior before enabling it.

Risk: The security summary reports inconsistent disclosure about how often the background timer runs.

Mitigation: Confirm the actual timer frequency in the installed systemd unit and communicate that frequency clearly before relying on auto-restart behavior.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/stigg86/skills/doctor-call)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or run OpenClaw diagnostics, repair commands, and user-level systemd timer configuration.]

## Skill Version(s):

1.3.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
