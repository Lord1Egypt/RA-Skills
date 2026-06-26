## Description: <br>
基于热量差=目标步数的核心理念，通过定时提醒、饮食打卡、步数督促、数据分析、激励机制陪伴用户健康减肥。支持8+16断食、加餐记录、平台期解释、体重趋势预测和多轮对话优化。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[joeyoung310](https://clawhub.ai/user/joeyoung310) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to run a local diet companion workflow for calorie estimates, meal logging, step tracking, weight trends, reminders, and progress summaries. It is intended for wellness tracking and does not replace medical advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores weight, meal, activity, and body-metric history as plaintext files in its local data directory. <br>
Mitigation: Use it only on trusted single-user machines, avoid shared workspaces, and delete the local data folder when those records should no longer be retained. <br>
Risk: Calorie estimates, fasting suggestions, and weight-loss summaries may be incomplete or unsuitable for users with medical conditions. <br>
Mitigation: Treat outputs as wellness tracking guidance only and consult a qualified health professional for medical or condition-specific advice. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/joeyoung310/ai-companion-diet) <br>
- [Publisher profile](https://clawhub.ai/user/joeyoung310) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Terminal text plus local JSON records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and updates plaintext local data files for user profile, daily meal and step records, and weight history.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
