## Description: <br>
Builds automation workflows from repetitive tasks. Use when user mentions "automate", "save time", "reduce manual work", or has repeated tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xaiohuangningde](https://clawhub.ai/user/xaiohuangningde) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, operators, and productivity-focused users use this skill to identify repeated manual work and turn it into automation workflows, scripts, and configuration. It is suited for tasks such as recurring report generation, scheduled data collection, and repeatable operational routines. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may encourage an agent to create or run automation scripts without clear approval gates. <br>
Mitigation: Require explicit user confirmation before executing generated scripts or applying generated configuration. <br>
Risk: Automation workflows may include scheduled jobs or automatic email/message sending. <br>
Mitigation: Review schedules, recipients, message content, and rollback steps before enabling any recurring or outbound action. <br>
Risk: Generated workflows may touch credentials, private files, or operational systems. <br>
Mitigation: Limit file and credential access to the minimum required scope and verify each data source before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xaiohuangningde/auto-workflow) <br>
- [Publisher profile](https://clawhub.ai/user/xaiohuangningde) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown plans with script, command, or configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose executable automation, scheduled jobs, or message-sending workflows; review and approve before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
