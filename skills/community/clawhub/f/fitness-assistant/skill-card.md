## Description:

Plan daily meals and workouts from a user's age and health profile with customizable ingredients, then schedule localized plans via OpenClaw automations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[l1mufeng](https://clawhub.ai/user/l1mufeng)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to create personalized one-day meal and workout plans, estimate daily food costs when a budget is provided, and schedule recurring daily plans or weekly recaps in a supported language.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may save sensitive health, body, dietary, budget, routine, timezone, and workout-log details in agent memory for reuse.

Mitigation: Review what profile data will be stored before installation, collect only needed fields, and provide a clear way to review or delete saved profile data when the platform supports it.

Risk: Recurring daily or weekly automations may deliver fitness content without sufficient user awareness if schedule details are not confirmed.

Mitigation: Enable scheduled delivery only after confirming the destination, timezone, recurrence, and next run time, and update existing jobs instead of creating duplicates.

Risk: Meal and workout plans can be inappropriate for minors, pregnancy, chronic conditions, medication interactions, injuries, or other health limitations.

Mitigation: Keep guidance general, adapt conservatively from reported constraints, avoid diagnosis or guaranteed outcomes, and recommend professional consultation for higher-risk profiles.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/l1mufeng/skills/fitness-assistant)
- [Server-resolved GitHub source](https://github.com/L1MuFeng/fitness-assistant-skill/tree/main/skills/fitness-assistant)
- [Daily ingredient cost budget](references/budget.md)
- [Dialogue scripts](references/dialogues.md)
- [Output languages](references/languages.md)
- [Meal planning rules](references/meal-planning.md)
- [Opening message and intake](references/opening.md)
- [User profile](references/profile.md)
- [Scheduling the daily plan](references/scheduling.md)
- [Workout planning rules](references/training.md)
- [Weekly summary](references/weekly-summary.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown fitness plans and summaries with optional shell commands and JSON calculator output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports eight output languages and recurring automation prompts when scheduling is requested.]

## Skill Version(s):

0.1.5 (source: ClawHub release metadata; artifact frontmatter reports 0.1.7)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
