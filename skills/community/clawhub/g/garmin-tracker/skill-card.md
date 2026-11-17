## Description:

Rebuild and maintain garmin_tracking.json from Garmin web data (activities + training plan) with a fixed schema from 2026-02-01.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ricardotrevisan](https://clawhub.ai/user/ricardotrevisan)

### License/Terms of Use:


## Use Case:

Runners and Garmin users use this skill to sync, rebuild, and validate a workspace garmin_tracking.json file from Garmin activity and training-plan data. It keeps history, summary metrics, current week, and upcoming workouts aligned to the skill's fixed schema.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use an authenticated Garmin browser session and update garmin_tracking.json.

Mitigation: Use a dedicated browser profile and a workspace containing only the intended tracking file; review changes before relying on the updated data.

Risk: Credentials mode accepts a Garmin password through command-line flags.

Mitigation: Prefer browser or manual login mode, avoid credentials mode when possible, and do not pass passwords on the command line.

## Reference(s):

- [Garmin Tracker on ClawHub](https://clawhub.ai/ricardotrevisan/skills/garmin-tracker)
- [Garmin Connect sign-in](https://connect.garmin.com/signin/)
- [Garmin Connect training plan](https://connect.garmin.com/app/training-plan)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON file updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces and validates garmin_tracking.json; helper scripts may emit JSON status, warnings, or normalized tracking data.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
