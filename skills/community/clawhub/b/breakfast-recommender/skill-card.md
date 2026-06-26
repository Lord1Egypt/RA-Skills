## Description: <br>
智能早餐推荐助手，根据冰箱食材推荐早餐、管理食材、记录偏好与历史。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sophiayuan1984-jpg](https://clawhub.ai/user/sophiayuan1984-jpg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to manage local breakfast ingredients, dietary preferences, and recommendation history, then receive simple breakfast suggestions based on what is available. It also supports read-only fridge checks, expiring-ingredient review, and optional scheduled breakfast recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may keep local records of fridge contents, breakfast history, and dietary preferences or allergies. <br>
Mitigation: Review or delete files under ~/.openclaw/workspace/breakfast-recommender/ when they become outdated, and avoid storing sensitive dietary details unless needed for recommendations. <br>
Risk: Scheduled recommendations can create recurring agent messages. <br>
Mitigation: Enable scheduled recommendations only when recurring messages are desired, and confirm the configured time and cancellation path. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/sophiayuan1984-jpg/breakfast-recommender) <br>
- [Publisher Profile](https://clawhub.ai/user/sophiayuan1984-jpg) <br>
- [fridge.md](references/fridge.md) <br>
- [history.md](references/history.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Configuration, Guidance] <br>
**Output Format:** [Markdown recommendations, tables, confirmations, and local Markdown record updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local fridge, preference, and recommendation-history files under ~/.openclaw/workspace/breakfast-recommender/.] <br>

## Skill Version(s): <br>
1.2.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
