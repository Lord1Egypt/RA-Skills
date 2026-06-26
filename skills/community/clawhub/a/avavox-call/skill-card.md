## Description: <br>
通过 大模型语音数字员工-avavox的外呼机器人的技能, 用于在 小龙虾(OpenClaw)等 Agent平台中实现大模型语音外呼机器人。适用于批量外呼、客户回访、满意度调查、简历筛查约面试，以及定时提醒、任务安排等场景。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[polandeme](https://clawhub.ai/user/polandeme) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to manage Avavox outbound-calling workflows from an agent environment, including selecting published robots, creating or updating tasks, importing customer lists, and pausing or resuming calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: App Key exposure could grant access to the Avavox space used by the skill. <br>
Mitigation: Store the App Key in protected OpenClaw credential or environment injection when possible, avoid hardcoding real keys in config.json, and do not echo complete keys in user-visible output. <br>
Risk: Incorrect phone-number lists, schedules, robot selection, line selection, or concurrency can trigger unintended outbound calls. <br>
Mitigation: Require explicit user review before importing customers or resuming calls, and verify available robots with robots list before every task creation. <br>
Risk: Customer phone data and ext variables may contain sensitive personal or business information. <br>
Mitigation: Review customer payloads before import, keep ext fields limited to required robot variables, and use tasks variables so the agent maps values to the documented variable names. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/polandeme/avavox-call) <br>
- [Avavox App Key documentation](https://avavox.com/avavox-docs/developer/app-key.html) <br>
- [Avavox create task documentation](https://avavox.com/avavox-docs/developer/create-task.html) <br>
- [Authentication and context reference](references/auth-and-context.md) <br>
- [Entity and endpoint map](references/entity-and-endpoint-map.md) <br>
- [Payload examples](references/payload-examples.md) <br>
- [Callback schema](references/callback-schema.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown guidance with shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Python standard-library commands that call Avavox open API endpoints under https://dashboard.avavox.com/open/api.] <br>

## Skill Version(s): <br>
0.6.2 (source: server release evidence and SKILL.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
