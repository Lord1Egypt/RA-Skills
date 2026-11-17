## Description:

A life-check skill that periodically checks whether the user is responsive, asks if they are okay after a timeout, and can notify emergency contacts by email if there is no reply.

This skill is ready for commercial/non-commercial use.

## Publisher:

[trae1oung](https://clawhub.ai/user/trae1oung)

### License/Terms of Use:


## Use Case:

External users can use this skill to set up a periodic personal check-in workflow that asks for confirmation after inactivity and prepares emergency email notification when the user remains unresponsive.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent cron execution can trigger unattended check-in behavior and notification preparation on a schedule.

Mitigation: Use a fixed trusted script path in cron, review the installed cron entry, and test the check-in flow before relying on it.

Risk: SMTP credentials and emergency contact configuration may be stored in plaintext configuration files.

Mitigation: Use a dedicated revocable SMTP app password and restrict the ~/.openclaw/apps/deadornot directory and config file to owner-only permissions.

Risk: The notification flow could contact the wrong recipient or send unexpected message content if configuration is incorrect.

Mitigation: Require an explicit opt-in setup flow that previews recipients and message content before enabling emergency email behavior.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local check-in state files and email configuration under the user's home directory when installed and configured.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
