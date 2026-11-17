## Description:

Coordinates specialized agents for complex tasks by planning team formation, execution order, progress tracking, and synthesis across parallel, sequential, hybrid, or adaptive workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mtsatryan](https://clawhub.ai/user/mtsatryan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to plan, coordinate, monitor, and synthesize work across multiple specialized agents for complex tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad multi-agent activation may be unnecessary for simple tasks.

Mitigation: Review the coordination plan and limit execution to the agents and phases that are justified by the task.

Risk: Selected agents may receive shared task context during coordination.

Mitigation: Check the plan before execution and avoid routing sensitive context to agents that do not need it.

## Reference(s):

- [Multi-Agent Coordinator Examples](references/examples.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown coordination plans, execution summaries, and final synthesis reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include proposed agent roles, execution phases, quality metrics, outstanding items, and recommended next steps.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
