## Description:

Automatically notifies when the gateway restarts by detecting a recovery flag and sending an "I'm back!" message during heartbeat checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kazuninishiki](https://clawhub.ai/user/kazuninishiki)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to have an agent detect gateway recovery during heartbeat checks and send a short automatic recovery notification after a restart.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic recovery messages may be sent to unintended recipients or at an unexpected frequency.

Mitigation: Before installing, verify the notification recipient, heartbeat cadence, and recovery-flag clearing behavior.

Risk: Persistent startup and heartbeat behavior may leave local files, logs, or LaunchAgent configuration in place longer than intended.

Mitigation: Review the LaunchAgent install and removal steps, flag file path, log path, and file permissions before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kazuninishiki/skills/gateway-recovery)
- [Publisher profile](https://clawhub.ai/user/kazuninishiki)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with inline shell commands and configuration paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces an automatic recovery notification and describes local flag, LaunchAgent, and log paths.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
