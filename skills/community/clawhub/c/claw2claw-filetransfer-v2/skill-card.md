## Description:

Cross-platform file transfer between OpenClaw agents via rsync over SSH for syncing, backup, and transfer tasks between agents on different machines.

This skill is ready for commercial/non-commercial use.

## Publisher:

[christopher-schulze](https://clawhub.ai/user/christopher-schulze)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to produce shell commands and configuration guidance for transferring, backing up, listing, and synchronizing files between OpenClaw agents over SSH with rsync.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can normalize persistent SSH access, including root access, between machines.

Mitigation: Use a dedicated unprivileged transfer account, verify exactly which SSH key is installed, and keep a clear revocation path.

Risk: Sync commands can delete files on the destination or copy broad sensitive paths to another machine.

Mitigation: Prefer dry-run before sync, scope transfer paths narrowly, and avoid broad paths such as /home, /etc, logs, or database dumps unless the destination is trusted and protected.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/christopher-schulze/skills/claw2claw-filetransfer-v2)
- [Command Reference](references/commands.md)
- [Real-World Examples](references/examples.md)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include rsync and SSH commands that transfer, mirror, or list local and remote files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
