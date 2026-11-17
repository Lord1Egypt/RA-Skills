## Description:

AI Running Coach provides Chinese-language marathon and half-marathon training guidance, including personalized plans, VDOT-based pace and heart-rate zones, TCX/GPX run analysis, race strategy, and training questions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kinsonhu123-mkll](https://clawhub.ai/user/kinsonhu123-mkll)

### License/Terms of Use:

MIT-0

## Use Case:

External runners and coaches use this skill to generate marathon training plans, calculate training zones, analyze run files, and prepare race pacing and fueling strategies. It is especially oriented toward Chinese-language coaching workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Training, injury, caffeine, salt, and fueling advice may not fit an individual runner's medical needs or race conditions.

Mitigation: Treat coaching output as general guidance, adjust it to personal condition and experience, and seek qualified medical advice for persistent pain, injury, or health concerns.

Risk: TCX/GPX parsing depends on file structure and may fail or produce incomplete summaries when activity data is missing or malformed.

Mitigation: Use trusted activity files, avoid very large or untrusted XML uploads, and review generated summaries before changing training decisions.

Risk: VDOT, pace, heart-rate, and weekly mileage calculations are estimates that may overstate safe training load for some runners.

Mitigation: Use the generated zones and plans as starting points, keep mileage progression conservative, and prioritize recovery when fatigue or pain appears.

## Reference(s):

- [AI Running Coach on ClawHub](https://clawhub.ai/kinsonhu123-mkll/skills/airunningcoach)
- [Publisher profile](https://clawhub.ai/user/kinsonhu123-mkll)
- [Training Zones](references/training-zones.md)
- [Workout Types](references/workout-types.md)
- [Race Strategies](references/race-strategies.md)
- [Weekly Plan Template](assets/weekly-plan-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown guidance with optional JSON or text output from local Python scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces coaching recommendations, training tables, pace and heart-rate zones, run summaries, and race plans.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
