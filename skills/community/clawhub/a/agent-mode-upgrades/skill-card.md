## Description:

Enhanced agentic loop with planning, parallel execution, confidence gates, semantic error recovery, and observable state machine.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maverick-software](https://clawhub.ai/user/maverick-software)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to add an enhanced OpenClaw agent loop with persistent planning, parallel execution, confidence gates, semantic error recovery, checkpointing, and dashboard configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill wraps agent behavior and can affect agents with broad tool access.

Mitigation: Review before enabling on production agents, enable per agent through the Mode dashboard, and test with least-privilege tool access first.

Risk: Approval timeouts can allow risky actions to proceed if left in the documented fail-open posture.

Mitigation: Configure or patch approval timeouts to deny on timeout for sensitive environments and keep high/critical approval gates enabled.

Risk: The skill reuses host LLM credentials and provider access.

Mitigation: Limit host auth profiles to approved providers and verify child environments do not expose stale or unintended credentials.

Risk: Local plan state and checkpoints may contain sensitive task context.

Mitigation: Protect the local OpenClaw state directory, prune checkpoints when no longer needed, and avoid enabling memory injection where sensitive data should not be reused.

Risk: The installed hook may differ from the documented integration.

Mitigation: Verify the installed hook and Mode dashboard integration match the packaged documentation before relying on enhanced-loop behavior.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/maverick-software/skills/agent-mode-upgrades)
- [README](artifact/README.md)
- [Security & Trust Documentation](artifact/SECURITY.md)
- [Integration Guide](artifact/INSTRUCTIONS.md)
- [Planning and Self-Reflection](artifact/references/planning-reflection.md)
- [Parallel Tool Execution](artifact/references/parallel-execution.md)
- [Confidence-Gated Autonomy](artifact/references/confidence-gates.md)
- [Semantic Error Recovery](artifact/references/error-recovery.md)
- [Proactive Context Management](artifact/references/context-management.md)
- [Observable State Machine](artifact/references/state-machine.md)
- [Hierarchical Task Management](artifact/references/task-hierarchy.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and structured plan/status text with TypeScript APIs, shell commands, and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces additive plan context, progress/status events, local checkpoint state, and Mode dashboard configuration when enabled.]

## Skill Version(s):

2.4.1 (source: server release and artifact/skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
