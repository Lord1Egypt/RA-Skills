## Description: <br>
Execution Loop provides stop-hook patterns and helper scripts that keep agents working through complex tasks, require concrete completion evidence, re-anchor long sessions, and configure headless execution budgets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lanyasheng](https://clawhub.ai/user/lanyasheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to manage long-running agent work, prevent premature stops, require evidence before completion, and keep execution aligned with the original task. It is most relevant for multi-step coding, migration, and verification workflows where Stop hooks or headless turn limits are part of the agent runtime. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can influence when an agent is allowed to stop by using local Stop hooks and state files. <br>
Mitigation: Install it only for workflows where deliberate Stop-hook control is desired, and review hook behavior before deployment. <br>
Risk: Session state may persist locally under shared context directories. <br>
Mitigation: Use clear session IDs without path characters, keep state directories private and out of source control, and clean old session data when it is no longer needed. <br>
Risk: Re-anchor and handoff patterns may persist sensitive prompt context locally. <br>
Mitigation: Avoid enabling those patterns for highly sensitive prompts unless local persistence is acceptable. <br>


## Reference(s): <br>
- [Execution Loop Skill Page](https://clawhub.ai/lanyasheng/execution-loop) <br>
- [Pattern 1.1: Ralph Persistent Loop](references/ralph.md) <br>
- [Pattern 1.2: Doubt Gate](references/doubt-gate.md) <br>
- [Pattern 1.3: Adaptive Complexity Scoring](references/adaptive-complexity.md) <br>
- [Task Completion Verifier](references/task-completion.md) <br>
- [Drift Re-anchoring](references/drift-reanchor.md) <br>
- [Headless Execution Control](references/headless-config.md) <br>
- [Iteration-Aware Block Messaging](references/iteration-aware-messaging.md) <br>
- [Cancel Signal with TTL](references/cancel-ttl.md) <br>
- [Execution Loop Extended Patterns](references/extended-patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with Bash commands, JSON hook outputs, and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes helper scripts that read and write local session state for Stop-hook workflows.] <br>

## Skill Version(s): <br>
2.4.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
