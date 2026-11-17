## Description:

Adaptive 12-week training plan generator using Garmin Connect data that creates structured workouts and schedules them on a Garmin calendar.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bpauli](https://clawhub.ai/user/bpauli)

### License/Terms of Use:

MIT-0

## Use Case:

External Garmin users and their agents use this skill to analyze Garmin Connect data, choose a training philosophy, generate an adaptive 12-week training plan, and schedule workouts for races or general fitness.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill needs access to Garmin fitness and calendar data and can create scheduled workouts.

Mitigation: Review the generated training plan and the planned Garmin actions before authorizing scheduling.

Risk: The skill can remove future Garmin workouts based on a simple W-prefix naming convention.

Mitigation: On re-runs, require the agent to show the exact workouts it plans to remove and approve deletion before any removal, especially for W-prefixed workouts the user may have created.

## Reference(s):

- [gccli command reference](references/gccli-commands.md)
- [gccli project](https://github.com/bpauli/gccli)
- [Garmin Trainer ClawHub listing](https://clawhub.ai/bpauli/skills/garmin-trainer)
- [bpauli ClawHub profile](https://clawhub.ai/user/bpauli)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown plan summaries with inline gccli command usage]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read Garmin fitness and calendar data and create, schedule, or remove Garmin workouts when authorized.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
