## Description: <br>
AI-powered meal photo recognition and nutrition tracking for calorie and macro analysis, daily summaries, weekly diet trends, health scoring, corrections, duplicate detection, and customizable nutrition goals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yxjsxy](https://clawhub.ai/user/yxjsxy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and personal nutrition-tracking agents use FoodLens to analyze meal photos, log food intake, and summarize daily or weekly nutrition trends. It is intended for calorie and macro tracking, not for medical diagnosis or treatment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Meal photos may be processed by an external AI provider. <br>
Mitigation: Use only with informed users, review the configured provider's data handling terms, and avoid submitting sensitive images unless that processing is acceptable. <br>
Risk: Nutrition history is stored locally in daily JSON logs. <br>
Mitigation: Store logs in a private location, restrict file access, and define a deletion or retention process before routine use. <br>
Risk: The release references local Python files that are not included in the artifact. <br>
Mitigation: Review or obtain the required Python files before execution, and do not run the skill until the local code and dependencies are trusted. <br>
Risk: Nutrition estimates and health scores can be inaccurate or misunderstood. <br>
Mitigation: Present results as estimates, support user corrections, and avoid using the output as medical or clinical advice. <br>


## Reference(s): <br>
- [FoodLens on ClawHub](https://clawhub.ai/yxjsxy/foodlens) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, JSON, guidance] <br>
**Output Format:** [Markdown-style nutrition reports with optional shell commands and JSON meal log records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May append meal records to local daily JSON logs and produce daily or weekly summary text.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
