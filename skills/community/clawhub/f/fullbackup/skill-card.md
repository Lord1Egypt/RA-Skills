## Description:

Create a full local backup of the OpenClaw workspace and configuration using the existing backup-local.sh script.

This skill is ready for commercial/non-commercial use.

## Publisher:

[trumppo](https://clawhub.ai/user/trumppo)

### License/Terms of Use:


## Use Case:

OpenClaw operators and developers use this skill to run a local full backup of the workspace and configuration and receive the resulting archive path and size.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill delegates the backup operation to an external local script outside the reviewed package.

Mitigation: Install and run it only after confirming that /root/.openclaw/workspace/scripts/backup-local.sh is trusted, executable, and aligned with the intended backup scope.

Risk: A full backup may archive sensitive workspace or configuration data into durable local files.

Mitigation: Confirm destination permissions, retention expectations, and secret-handling policy before running the backup.

## Reference(s):


## Skill Output:

**Output Type(s):** [shell commands, files, text]

**Output Format:** [Local archive file plus text status output with the archive path and size]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Delegates execution to the local backup script configured on the host.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
