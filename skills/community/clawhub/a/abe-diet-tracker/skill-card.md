## Description: <br>
Tracks daily diet and calculates nutrition information to help achieve weight loss goals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abeltennyson](https://clawhub.ai/user/abeltennyson) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to log meals, calculate calories and macronutrients, check remaining daily nutrition budgets, and receive lunch or dinner logging reminders. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads local body, activity, calorie, and macronutrient profile data. <br>
Mitigation: Install only when that local profile access is acceptable, and keep USER.md limited to data needed for diet tracking. <br>
Risk: Meal queries may be sent to SkillBoss when the local nutrition database does not contain a food item. <br>
Mitigation: Provide only meal details you are comfortable sending to the external nutrition lookup service, or rely on local nutrition data where possible. <br>
Risk: Diet logs are stored locally and may be copied to an Obsidian vault and pushed with local Git credentials. <br>
Mitigation: Disable or remove Obsidian/GitHub sync unless you explicitly want those logs and vault changes committed and pushed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/abeltennyson/abe-diet-tracker) <br>
- [Food database reference](references/food_database.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown diet logs, nutrition summaries, reminder text, and command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include calorie and macronutrient estimates, remaining budget calculations, and local log updates.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
