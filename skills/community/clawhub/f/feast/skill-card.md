## Description:

Feast helps agents create personalized weekly meal plans with regional recipes, season-aware shopping lists, dietary guidance, and curated mealtime playlists.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smadgerano](https://clawhub.ai/user/smadgerano)

### License/Terms of Use:

MIT

## Use Case:

External users use Feast with OpenClaw agents to plan weekly meals, generate shopping lists, adapt recipes to dietary and regional preferences, and create themed mealtime experiences. The skill supports onboarding, recurring planning, daily meal reveal, shopping, and review workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recurring background reminders and optional external notification delivery may send meal-planning information outside the local chat context.

Mitigation: Review notification settings before installation, use webchat or local delivery by default, and enable Telegram, Discord, Signal, Pushbullet, or ntfy only when intentionally configured.

Risk: Meal profiles can contain dietary, health, household, location, and shopping-preference details.

Mitigation: Store only the details needed for meal planning and avoid unnecessary sensitive health or household information.

Risk: Feast cron jobs can continue producing planning or reveal reminders after the user stops using the skill.

Mitigation: Remove Feast cron jobs when disabling the skill or changing notification preferences.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/smadgerano/skills/feast)
- [OpenClaw](https://openclaw.ai)
- [Specification](docs/SPECIFICATION.md)
- [Onboarding Guide](references/onboarding.md)
- [Theme Research Guide](references/theme-research.md)
- [Price Checking Guide](references/price-checking.md)
- [Nutrition Guidelines](references/nutrition.md)
- [Unit Conversions Reference](references/conversions.md)
- [Cultural Events Calendar](references/events.md)
- [Seasonality Guides](references/seasonality/)
- [Cuisine Guides](references/cuisines/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Shell commands, Guidance]

**Output Format:** [Markdown meal plans and shopping lists with YAML profile and week-plan data, plus optional shell commands for history updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update user workspace meal-planning files and recurring reminder configuration when the user enables notifications.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
