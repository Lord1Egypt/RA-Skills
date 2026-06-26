## Description: <br>
飞书端读取USER.md任务清单。当用户说"查看任务"、"我的任务"时触发，实时解析并返回格式化的分类任务列表，让用户快速了解当前所有可用任务和技能。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[349840432m-dev](https://clawhub.ai/user/349840432m-dev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and OpenClaw users use this skill to read a local USER.md task list from Feishu and receive a categorized view of scheduled automations, available tasks, skill names, descriptions, and trigger phrases. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Feishu users who can invoke the skill may see task names, schedules, skill names, and trigger phrases from USER.md. <br>
Mitigation: Install only where that visibility is acceptable, avoid storing secrets or private notes in USER.md, and review shared-chat access before enabling the skill. <br>
Risk: Generic triggers such as 帮助 or ? may expose the task list in shared Feishu conversations. <br>
Mitigation: Narrow or remove generic triggers when the skill is used in shared chats. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/349840432m-dev/feishu-user-md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, guidance] <br>
**Output Format:** [Plain text or JSON generated from local Markdown table data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads ~/.openclaw/workspace/USER.md at invocation time and does not cache output.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact metadata lists 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
