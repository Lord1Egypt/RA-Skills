## Description:

Daily Meal Planner helps an agent recommend daily or weekly meals based on meal time, taste, mood, season, weather, region, nutrition goals, and stored preferences.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gmmg55](https://clawhub.ai/user/gmmg55)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to have an agent plan meals, search for recipes, and tailor recommendations to the user's meal time, weather, location, mood, preferences, allergies, and diet goals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may download recipe data from GitHub/jsDelivr and query wttr.in or date.nager.at, which can expose city and runtime context to external services.

Mitigation: Run it in a sandboxed environment, pre-bundle or verify recipe JSON files, and review or limit network access before use.

Risk: Preferences such as location, allergies, diet goals, and taste may be stored locally in user_profile.json.

Mitigation: Delete user_profile.json when persistence is not desired and avoid entering sensitive personal information.

## Reference(s):

- [Daily Meal Planner ClawHub listing](https://clawhub.ai/gmmg55/skills/daily-meal-planner)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, guidance]

**Output Format:** [Markdown meal recommendations and JSON context for daily or weekly planning.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use locally cached recipe data and locally persisted user_profile.json preferences.]

## Skill Version(s):

1.3.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
