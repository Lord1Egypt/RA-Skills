## Description:

通过 大模型语音数字员工-avavox的外呼机器人的技能, 用于在 小龙虾(OpenClaw)等 Agent平台中实现大模型语音外呼机器人。适用于批量外呼、客户回访、满意度调查、简历筛查约面试，以及定时提醒、任务安排等场景。

This skill is ready for commercial/non-commercial use.

## Publisher:

[polandeme](https://clawhub.ai/user/polandeme)

### License/Terms of Use:

MIT-0

## Use Case:

External operators, support teams, recruiters, and developers use this skill to manage Avavox outbound-calling workflows from an agent: list published robots and lines, create or update call tasks, import customer phone lists, and inspect task variables before passing customer context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles customer phone numbers and optional ext fields that may contain personal or business-sensitive data.

Mitigation: Import only customer data that the operator is authorized to send to Avavox, and minimize ext fields to the values needed by the selected robot.

Risk: A broad or stored App Key could allow unintended task operations if exposed or reused outside the intended workspace.

Mitigation: Use a narrowly scoped Avavox App Key when available, prefer environment injection over real keys in config.json, and avoid printing full keys in user-visible output.

Risk: Misconfigured robot, line, schedule, concurrency, or retry settings could trigger unwanted outbound calls.

Mitigation: List and confirm the current robot and line before task creation, verify call windows and concurrency, and import customers only after the final task configuration is reviewed.

Risk: The restricted request fallback can make API changes for endpoints that do not have first-class command wrappers.

Mitigation: Keep fallback requests under documented /open/api paths, review method, path, query, and body values before execution, and prefer wrapped commands where available.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/polandeme/skills/avavox-call)
- [Avavox App Key documentation](https://avavox.com/avavox-docs/developer/app-key.html)
- [Avavox create task documentation](https://avavox.com/avavox-docs/developer/create-task.html)
- [Authentication and context](references/auth-and-context.md)
- [Entity and endpoint map](references/entity-and-endpoint-map.md)
- [Payload examples](references/payload-examples.md)
- [Callback schema](references/callback-schema.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON payloads and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses an Avavox App Key and sends JSON requests to Avavox open API endpoints.]

## Skill Version(s):

0.6.2 (source: server release evidence, artifact SKILL.md, and script constant)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
