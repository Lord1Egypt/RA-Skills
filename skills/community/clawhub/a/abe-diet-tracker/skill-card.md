## Description:

Tracks daily diet and calculates nutrition information to help achieve weight loss goals when users provide meal information, ask about calorie intake, request remaining calorie budget, or need meal logging reminders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abeltennyson](https://clawhub.ai/user/abeltennyson)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to log meals, estimate calories and macronutrients, track remaining daily nutrition budgets, and receive lunch or dinner logging reminders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Meal queries and nutrition context can be sent to SkillBoss during lookup.

Mitigation: Use the skill only when this data sharing is acceptable and ensure SKILLBOSS_API_KEY is configured for the intended account.

Risk: Diet logs and profile-derived nutrition data are stored locally.

Mitigation: Keep USER.md and memory files in an appropriate private workspace and review stored logs for sensitive health or personal data.

Risk: The artifact can synchronize an Obsidian vault and push Git changes, which may upload unrelated private notes.

Mitigation: Remove or explicitly configure the Obsidian and Git synchronization path before use, and review staged files before any push.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/abeltennyson/skills/abe-diet-tracker)
- [Food database](references/food_database.json)
- [SkillBoss API Hub](https://api.heybossai.com/v1)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and plain text with nutrition totals, remaining budgets, meal log entries, reminders, and command-oriented script usage.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read user profile data, call SkillBoss for nutrition estimates, and write daily diet logs.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
