## Description: <br>
Tracks daily diet and calculates nutrition information to help achieve weight loss goals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[YonghaoZhao722](https://clawhub.ai/user/YonghaoZhao722) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Individuals use this skill to log meals, estimate calories and macronutrients, check remaining daily nutrition budgets, and receive meal logging reminders. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Meal logging can write private diet notes locally, copy them into an Obsidian vault, and push the vault to a configured GitHub remote using existing Git credentials. <br>
Mitigation: Review before installing; remove or disable the Obsidian copy and git push behavior, or require explicit confirmation and restrict commits to the generated diet log file only. <br>


## Reference(s): <br>
- [Food database](references/food_database.json) <br>
- [ClawHub skill page](https://clawhub.ai/YonghaoZhao722/diet-tracker) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown and plain text status updates with generated diet log entries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write daily meal logs and nutrition summaries to local Markdown files.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
