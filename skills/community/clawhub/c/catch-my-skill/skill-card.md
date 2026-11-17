## Description:

Catch My Skill helps OpenClaw users track local skill versions against ClawHub versions and report when tracked skills are behind.

This skill is ready for commercial/non-commercial use.

## Publisher:

[russellfei](https://clawhub.ai/user/russellfei)

### License/Terms of Use:


## Use Case:

OpenClaw users and skill maintainers use this skill to initialize a tracked list of local skills, compare local versions with ClawHub versions, and identify skills that may need updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The update command can install mutable remote skill code and has an unvalidated shell-command path.

Mitigation: Use read-only check features unless the update path is fixed; verify update sources before installing remote skill code.

Risk: Recurring checks may run automatically if a cron job is enabled without clear operator consent.

Mitigation: Enable scheduled runs only with explicit opt-in and provide a clear way to remove or disable the cron job.

## Reference(s):

- [Catch My Skill on ClawHub](https://clawhub.ai/russellfei/skills/catch-my-skill)
- [russellfei ClawHub profile](https://clawhub.ai/user/russellfei)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text status reports with command examples and JSON state files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Maintains local and online skill-version lists in JSON files.]

## Skill Version(s):

1.0.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
