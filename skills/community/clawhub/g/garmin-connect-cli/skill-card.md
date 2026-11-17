## Description:

Garmin Connect CLI helps agents work with Garmin Connect activities, health, body composition, workouts, devices, gear, goals, and related account data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bpauli](https://clawhub.ai/user/bpauli)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to have an agent produce or run gccli commands for authenticated Garmin Connect account workflows, including activity, health, workout, course, device, gear, goal, and wellness tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill operates on authenticated Garmin Connect data, including sensitive health and fitness information.

Mitigation: Review before installing, use interactive login where possible, and avoid exporting tokens unless necessary.

Risk: Some supported workflows can upload, delete, schedule, or make course and event changes.

Mitigation: Confirm user intent before upload, delete, schedule, or public course/event changes.

Risk: Exported credentials or tokens could expose the Garmin account if stored insecurely.

Mitigation: Do not store exported credentials in plaintext and prefer the CLI's OS keyring-backed authentication flow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bpauli/skills/garmin-connect-cli)
- [Publisher profile](https://clawhub.ai/user/bpauli)
- [gccli source repository](https://github.com/bpauli/gccli)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [For programmatic command output, the skill instructs agents to prefer gccli JSON output.]

## Skill Version(s):

1.8.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
