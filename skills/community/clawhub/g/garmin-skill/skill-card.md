## Description:

Talk to your Garmin data — ask questions about your activities, training load, VO2 Max, heart rate zones, and more using AI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nftechie](https://clawhub.ai/user/nftechie)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to let an agent query Transition APIs for Garmin-derived activity, training, performance, workout, profile, and coach-chat information.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends sensitive Garmin-derived activity, performance, profile, schedule, and chat data to a third-party service.

Mitigation: Review the data-sharing posture before installation and use only with users who are comfortable granting Transition and the agent access to this data.

Risk: The Transition API key grants access to personalized Garmin-derived data.

Mitigation: Protect the API key like a password, avoid logging it, and store it only in appropriate secret or environment-variable handling.

Risk: The skill includes an action that can push workouts to Garmin.

Mitigation: Require explicit user confirmation before any push-to-Garmin action.

## Reference(s):

- [Garmin Skill on ClawHub](https://clawhub.ai/nftechie/skills/garmin-skill)
- [Transition](https://www.transition.fun)
- [Transition API Base URL](https://api.transition.fun)

## Skill Output:

**Output Type(s):** [Text, API Calls, Shell commands, Guidance]

**Output Format:** [Markdown with natural-language answers and inline HTTP examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use a Transition API key for personalized Garmin-derived data and an unauthenticated workout-of-the-day endpoint for generic workout generation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
