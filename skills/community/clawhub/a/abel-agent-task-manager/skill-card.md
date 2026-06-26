## Description: <br>
Manages and orchestrates multi-step, stateful agent workflows; handles task dependencies, persistent state, error recovery, and external rate-limiting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abeltennyson](https://clawhub.ai/user/abeltennyson) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation builders use this skill to define, resume, and coordinate multi-step agent workflows with dependencies, persistent state, rate limits, and optional notifications. It is suited to structured task automation where human requests need to become executable task plans. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Task descriptions, workflow data, notification text, and recipient details may be sent to the SkillBoss/HeyBoss API. <br>
Mitigation: Avoid secrets, regulated data, private business workflows, or unapproved contacts unless explicit confirmation, redaction, and recipient controls are added. <br>
Risk: The cooldown wrapper executes a provided command string and the workflow scripts can perform external API calls. <br>
Mitigation: Review commands and task definitions before execution, constrain allowed actions, and run the skill in an environment with only the required credentials. <br>
Risk: External API failures or model parsing errors can produce incomplete or fallback task results. <br>
Mitigation: Validate parsed task JSON and workflow results before using them for notifications or follow-on actions. <br>


## Reference(s): <br>
- [Task Structure Schema](references/task_schema.md) <br>
- [SkillBoss API Hub /v1 API](https://api.heybossai.com/v1) <br>
- [SkillBoss API Hub /v1/pilot Endpoint](https://api.heybossai.com/v1/pilot) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown guidance with JSON task definitions and shell/Python command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call the SkillBoss/HeyBoss API and write local task state files when the included scripts are executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
