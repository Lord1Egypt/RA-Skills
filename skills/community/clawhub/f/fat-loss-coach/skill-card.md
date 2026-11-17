## Description:

Fat Loss Coach helps an agent calculate calorie targets, draft meal and workout plans, track progress, and answer fat-loss questions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smallkeyboy](https://clawhub.ai/user/smallkeyboy)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill with an agent to estimate BMR/TDEE, set calorie and macronutrient targets, generate meal and workout plans, and track fat-loss progress. The skill is best treated as general wellness guidance rather than medical, nutrition, or training advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can store sensitive weight, body measurement, diet, exercise, and health-condition notes in local memory.

Mitigation: Ask for explicit confirmation before saving a profile, minimize collected health details, and avoid storing detailed medical history unless it is necessary for the user's request.

Risk: Diet, fasting, and workout guidance may be unsuitable for people with medical conditions, pregnancy, injuries, eating-disorder history, diabetes, or minors.

Mitigation: Present plans as general guidance and recommend review by a qualified clinician, dietitian, or trainer for higher-risk users.

Risk: Calorie, macronutrient, and progress calculations are estimates that can mislead users when inputs or trends are incomplete.

Mitigation: State that calculations are estimates, request current inputs, monitor trend data and wellbeing signals, and adjust plans conservatively.

## Reference(s):

- [Fat Loss Coach ClawHub page](https://clawhub.ai/smallkeyboy/skills/fat-loss-coach)
- [Calculation formulas](references/formulas.md)
- [Recommended foods and cautions](references/foods.md)
- [Meal plan examples](references/meal-plans.md)
- [Workout plans](references/workout-plans.md)
- [Progress tracking and analysis](references/tracking.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, local markdown profile updates, shell command examples, and optional JSON from the calculation helper]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update a local user profile containing body, diet, exercise, health-condition, and progress data.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
