## Description:

Provides a 10-second automatic rollback and restart path for OpenClaw Gateway when configuration changes cause the Gateway to fail.

This skill is ready for commercial/non-commercial use.

## Publisher:

[segasonicye](https://clawhub.ai/user/segasonicye)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw operators use this skill while editing openclaw.json to recover from failed configuration changes by restoring the newest backup and restarting the Gateway.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The watchdog may overwrite the active OpenClaw configuration with the newest backup when the Gateway status check fails.

Mitigation: Review and protect the contents of ~/.openclaw/backups before enabling it, and keep a known-good backup for rollback.

Risk: A forced Gateway restart can interrupt service during recovery.

Mitigation: Run it during planned configuration changes and monitor Gateway recovery before using it unattended.

Risk: The runtime scope and safeguards are unclear.

Mitigation: Limit use to the intended backup or configuration-change window until the operating environment has been reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/segasonicye/skills/claw-seatbelt)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown guidance with shell command examples and local script behavior]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May restore ~/.openclaw/openclaw.json from the newest backup and restart OpenClaw Gateway when the status check fails.]

## Skill Version(s):

0.1.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
