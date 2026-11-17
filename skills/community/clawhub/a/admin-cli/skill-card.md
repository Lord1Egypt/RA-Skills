## Description:

Command-line tool for performing system updates, restarting systemd services, and checking OS status with elevated privileges.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fabglitch](https://clawhub.ai/user/fabglitch)

### License/Terms of Use:


## Use Case:

Developers and system administrators use this skill to have an agent perform common Linux administration tasks, including package updates, systemd service restarts, and status checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can request privileged system updates or systemd service restarts.

Mitigation: Install only on trusted machines, review each privileged command before authorizing it, and avoid production use without normal change-control review.

Risk: The update command uses pacman and is therefore specific to systems that support that package manager.

Mitigation: Confirm the target host uses pacman before authorizing update-system.

## Reference(s):


## Skill Output:

**Output Type(s):** [Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may require elevated privileges and user authorization before execution.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
