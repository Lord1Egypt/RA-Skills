## Description: <br>
Daily Meal Planner helps an agent recommend meals from meal time, taste, mood, season, weather, location, and user preference context. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gmmg55](https://clawhub.ai/user/gmmg55) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill through an agent to plan daily meals, weekly menus, and recipe lookups with personalized dietary context. The skill is intended for meal suggestions and recipe guidance, not medical or nutrition advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can store a local food-preference profile that may include location and dietary preferences. <br>
Mitigation: Avoid entering precise location details, review the saved profile before sharing the workspace, and delete user_profile.json when persistence is not desired. <br>
Risk: The skill can contact external services for recipe data, weather, and holiday context. <br>
Mitigation: Run it only in environments where those network lookups are acceptable, and review downloaded recipe data before relying on it. <br>
Risk: Meal suggestions and nutrition fields may be incomplete or unsuitable for medical dietary constraints. <br>
Mitigation: Treat outputs as planning guidance and verify allergies, health restrictions, and nutrition needs before using a recommendation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gmmg55/daily-meal-planner) <br>
- [Publisher profile](https://clawhub.ai/user/gmmg55) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, guidance] <br>
**Output Format:** [Markdown responses and JSON context for daily or weekly meal planning] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include meal names, tags, ingredients, nutrition fields, weather context, profile preferences, and recipe-detail prompts.] <br>

## Skill Version(s): <br>
1.3.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
