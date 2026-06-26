## Description: <br>
Enhances an OpenClaw agent loop with planning, parallel execution, confidence gates, semantic error recovery, observable state, and a Mode dashboard for configuration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maverick-software](https://clawhub.ai/user/maverick-software) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and teams using OpenClaw use this skill to add persistent planning, state tracking, checkpointing, context management, and approval-aware execution to agent workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill changes the agent loop in high-impact ways and safety controls may not reliably require explicit approval before risky actions proceed. <br>
Mitigation: Review Mode settings, test on a non-production agent first, and avoid enabling it for unattended high-impact actions. <br>
Risk: Planning and summarization may send task details, tool outputs, and file paths to the configured LLM provider. <br>
Mitigation: Avoid use with sensitive local project data unless the configured provider and auth profile are approved for that data. <br>
Risk: Approval gates can proceed after a timeout for high-risk operations. <br>
Mitigation: Use stricter approval settings where explicit human approval is required for high or critical actions. <br>


## Reference(s): <br>
- [Agentic Loop Upgrade ClawHub Page](https://clawhub.ai/maverick-software/agent-mode-upgrades) <br>
- [Security and Trust Documentation](artifact/SECURITY.md) <br>
- [Integration Guide](artifact/INSTRUCTIONS.md) <br>
- [Confidence Gates](artifact/references/confidence-gates.md) <br>
- [Context Management](artifact/references/context-management.md) <br>
- [Error Recovery](artifact/references/error-recovery.md) <br>
- [Parallel Execution](artifact/references/parallel-execution.md) <br>
- [Planning and Reflection](artifact/references/planning-reflection.md) <br>
- [Observable State Machine](artifact/references/state-machine.md) <br>
- [Task Hierarchy](artifact/references/task-hierarchy.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with TypeScript examples, JSON configuration snippets, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local OpenClaw configuration, plan state, and checkpoint files when enabled by the host agent.] <br>

## Skill Version(s): <br>
2.4.1 (source: server release and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
