## Description:

Config Guardian helps agents update OpenClaw configuration with automatic backup, validation, and rollback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abdhilabs](https://clawhub.ai/user/abdhilabs)

### License/Terms of Use:


## Use Case:

Developers and agents maintaining OpenClaw installations use this skill to apply configuration changes while preserving backups and rolling back failed validation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Successful configuration changes can alter agent behavior.

Mitigation: Review requested config changes before approval and use the disclosed validation workflow before treating an update as complete.

Risk: A failed configuration update can leave OpenClaw unusable if recovery is not available.

Mitigation: Use the atomic apply workflow, which creates a timestamped backup and rolls back when validation fails; preserve backups for manual restore.

## Reference(s):

- [Config Guardian ClawHub listing](https://clawhub.ai/abdhilabs/skills/config-guardian)
- [abdhilabs publisher profile](https://clawhub.ai/user/abdhilabs)
- [ClawHub registry](https://clawhub.ai)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces agent-facing config update steps that should be reviewed before approval.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
