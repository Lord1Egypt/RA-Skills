## Description: <br>
Protocol for multi-agent collaboration via OpenClaw's message-passing and recursive task DAGs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[srikanth235](https://clawhub.ai/user/srikanth235) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use Clawflow to coordinate complex work across multiple OpenClaw agents by decomposing tasks into recursive DAGs, dispatching subtasks, tracking replies, and synthesizing final results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recursive delegation and fan-out can expand work across many peer agents without strong built-in limits. <br>
Mitigation: Use narrow OpenClaw subagent permissions, avoid wildcard delegation where possible, and set practical recursion and fan-out limits before use. <br>
Risk: Task context can be forwarded broadly to peer agents and retained in mailbox and task logs. <br>
Mitigation: Do not include secrets or sensitive business or personal data unless that data may be forwarded to reachable agents and retained in workspace logs. <br>
Risk: The skill depends on the behavior of peer agents it can reach. <br>
Mitigation: Install and run it only with trusted peer agents and review configured agent access before delegating work. <br>


## Reference(s): <br>
- [Clawflow Skill Definition](artifact/SKILL.md) <br>
- [Agent Loop](artifact/agent-loop.md) <br>
- [Coordinating](artifact/coordinating.md) <br>
- [Message & File Schemas](artifact/schemas.md) <br>
- [Clawflow Release Page](https://clawhub.ai/srikanth235/clawflow) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with YAML frontmatter examples, Python helper scripts, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces structured task and reply messages, task.md state files, mailbox/task workspace layout guidance, and OpenClaw CLI command patterns.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
