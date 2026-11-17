## Description:

Set up, audit, repair, or restore a six-hour Azure DevOps workspace backup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daniel-refahi-ikara](https://clawhub.ai/user/daniel-refahi-ikara)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators of Daniel-owned agents use this skill to establish, audit, repair, and restore scheduled workspace backups to an approved Azure DevOps remote.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive or unintended workspace files could be committed to the backup remote.

Mitigation: Confirm the allowlist and exclusions, inspect the first staged diff, and scan staged files for credentials before enabling backups.

Risk: Misconfigured credentials, remote branch, or notification target could disrupt backups or misdirect alerts.

Mitigation: Verify credential file permissions, the approved remote and branch, and the notification target before enabling the timer.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/daniel-refahi-ikara/skills/dr-agent-backup)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration]

**Output Format:** [Markdown with configuration and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports timer state, next trigger, backup and remote verification, notification policy, tracked scope, and limitations.]

## Skill Version(s):

1.0.4 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
