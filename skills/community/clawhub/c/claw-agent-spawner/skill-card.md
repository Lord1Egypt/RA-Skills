## Description:

Decompose complex tasks into independent subtasks, plan parallel sub-agent execution, and synthesize the collected results into a coherent deliverable.

This skill is ready for commercial/non-commercial use.

## Publisher:

[indigas](https://clawhub.ai/user/indigas)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to split complex research, coding, analysis, review, or documentation tasks into separable sub-agent assignments and then combine the results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Parallel sub-agents can increase execution cost and token usage.

Mitigation: Use the skill for complex, clearly separable work, limit the number of sub-agents, and set timeouts.

Risk: Multiple agents may read or modify the same workspace during a task.

Mitigation: Keep sub-agent instructions narrow, avoid shared mutable state, and review synthesized results before relying on them.

Risk: Poor task decomposition can create dependencies, duplicated work, or lossy synthesis.

Mitigation: Follow the documented spawn patterns, keep subtasks independent, and actively reconcile conflicts during final synthesis.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/indigas/skills/claw-agent-spawner)
- [Spawn Patterns Reference Guide](artifact/references/spawn-patterns.md)
- [Model Selection Guide](artifact/references/model-selection.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON spawn plans from the planner script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Planner output includes subtask descriptions, dependency hints, recommended model class, expected output format, and synthesis guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact version history)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
