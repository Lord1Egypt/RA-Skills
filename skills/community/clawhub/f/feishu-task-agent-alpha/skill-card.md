## Description: <br>
飞书任务智能体统一路由飞书任务编排、未开始任务轮询执行、智能体注册初始化和 daily.json 画像刷新。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luckyterry](https://clawhub.ai/user/luckyterry) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and developers using Feishu task workflows use this skill to turn actionable requests into Feishu tasks, manage recurring or polled work, initialize the Feishu task agent, and publish daily.json profile summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can install or update ongoing automations and scheduler behavior. <br>
Mitigation: Review cron jobs before enabling the skill, use a test workspace first, and require explicit approval for recurring jobs or scheduler changes. <br>
Risk: The skill can change future agent routing and Feishu profile update behavior. <br>
Mitigation: Review AGENTS.md routing changes and Feishu profile updates before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/luckyterry/feishu-task-agent-alpha) <br>
- [Feishu Auto Task Decision Rules](references/task-decision-rules.md) <br>
- [Creator / Members Output Contract](references/task-output-contract.md) <br>
- [Feishu Task Agent Examples](references/task-examples.md) <br>
- [daily.json Data Structure](references/profile-data-shape.md) <br>
- [Profile Discovery Rules](references/profile-discovery-rules.md) <br>
- [Profile Schedule Rules](references/profile-schedule-rules.md) <br>
- [Auto Task Workflow](workflows/auto-task.md) <br>
- [Polled Task Execution Workflow](workflows/polled-task-execution.md) <br>
- [Agent Profile Workflow](workflows/agent-profile.md) <br>
- [Registration Workflow](workflows/reg.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, JSON] <br>
**Output Format:** [Markdown guidance with shell command snippets and JSON payloads; profile output is daily.json.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update Feishu tasks, comments, attachments, cron jobs, routing files, and profile JSON when used by an agent.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
