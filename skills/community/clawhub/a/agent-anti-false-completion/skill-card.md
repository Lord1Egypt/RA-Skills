## Description: <br>
用于减少 AI agent 假完成行为，通过任务约束、结果校验和执行规范，帮助复杂任务保持真实执行、明确验证与可信交付。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[initail](https://clawhub.ai/user/initail) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and developers use this skill to reduce false completion by encouraging tool-based investigation, validation before completion claims, and structured handoff when a task cannot be fully resolved. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can encourage aggressive tool use, scope expansion, and delayed user clarification. <br>
Mitigation: Use it only where the agent must still respect user scope, explain what it checked, and ask before risky shell commands, network access, credential handling, or destructive operations. <br>
Risk: The skill's pressure language may push agents to continue beyond appropriate boundaries. <br>
Mitigation: Stop or escalate to the user when safety, legal, financial, medical, credential, or destructive-operation boundaries are involved. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/initail/agent-anti-false-completion) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands] <br>
**Output Format:** [Markdown guidance with checklists, escalation labels, and suggested verification actions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only skill; it may prompt agents to use available tools but does not bundle executable code.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
