## Description:

Create personalized daily plans using real calendar availability and priorities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aditiprasath](https://clawhub.ai/user/aditiprasath)

### License/Terms of Use:

MIT-0

## Use Case:

External users can organize tasks around calendar commitments, priorities, and estimated durations to get a proposed daily schedule and a list of tasks that could not be placed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Incomplete or unavailable calendar data can make a proposed schedule conflict with real commitments.

Mitigation: Use successfully retrieved calendar events, state assumptions when details are missing, and review the proposed schedule before relying on it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aditiprasath/skills/a3-daily-planner)

## Skill Output:

**Output Type(s):** [Text, Guidance, JSON]

**Output Format:** [Proposed daily schedule with task times and unscheduled tasks; the bundled planner utility emits JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Events, task durations, and priorities are provided as input; the plan does not save calendar events or send notifications.]

## Skill Version(s):

1.0.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
