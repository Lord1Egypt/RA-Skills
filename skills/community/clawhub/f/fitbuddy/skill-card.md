## Description: <br>
FitBuddy helps an agent log fitness, diet, weight, exercise, hydration, macro targets, progress reports, reminders, and optional restaurant nutrition data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[promisewhh](https://clawhub.ai/user/promisewhh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and their agents use this skill to maintain local fitness, diet, weight, hydration, and exercise logs, calculate calorie and macro targets, generate progress summaries, and receive reminders. It can also guide meal planning and optional restaurant nutrition lookup when the user enables those integrations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Fitness, diet, weight, and health-condition data may be sensitive even when stored locally. <br>
Mitigation: Keep fitbuddy-data local, avoid sharing records or screenshots, and review local retention or deletion expectations before use. <br>
Risk: Cron reminders and third-party messaging channels can send fitness or meal content outside the local workspace. <br>
Mitigation: Review reminder schedules and channel configuration before enabling them, and disable external channels when private reminders are not acceptable. <br>
Risk: Optional MCP or messaging integrations require tokens that could be exposed through screenshots, logs, or version control. <br>
Mitigation: Store tokens only in local configuration, redact them from logs and screenshots, and do not commit them to source control. <br>
Risk: Fitness and nutrition recommendations may be unsuitable for users with medical conditions or specialized dietary needs. <br>
Mitigation: Use the skill's conservative guardrails and seek qualified medical or nutrition advice before relying on the guidance for health-sensitive decisions. <br>


## Reference(s): <br>
- [ClawHub FitBuddy Release Page](https://clawhub.ai/promisewhh/fitbuddy) <br>
- [README](README.md) <br>
- [Initialization Guide](references/init-guide.md) <br>
- [Nutrition Guide](references/nutrition-guide.md) <br>
- [Nutrition Formulas](references/nutrition.md) <br>
- [Exercise Reference](references/exercise.md) <br>
- [Training Plan Reference](references/training-plan.md) <br>
- [Budget Meals Reference](references/budget-meals.md) <br>
- [Reports and Charts Reference](references/reports.md) <br>
- [Reminder Logic](references/reminder-logic.md) <br>
- [Reminder Channel Configuration](references/channels.md) <br>
- [McDonald's MCP Integration](references/mcd-integration.md) <br>
- [McDonald's MCP](https://open.mcd.cn/mcp) <br>
- [DingTalk Developer Console](https://open-dev.dingtalk.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, JSON files, Charts] <br>
**Output Format:** [Markdown responses with inline shell commands, JSON snippets, local JSON records, and generated chart image files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores profile, food database, daily records, user patterns, and generated charts under fitbuddy-data; optional reminders and MCP integrations require user configuration.] <br>

## Skill Version(s): <br>
2.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
