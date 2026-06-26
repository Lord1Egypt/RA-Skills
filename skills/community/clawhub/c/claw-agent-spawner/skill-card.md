## Description: <br>
Decompose complex tasks into independent subtasks, spawn parallel agents to execute them, and synthesize their outputs into a final deliverable. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[indigas](https://clawhub.ai/user/indigas) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to break multi-part research, coding, analysis, review, and documentation work into scoped sub-agent tasks, then collect and synthesize the results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Parallel sub-agents may overlap in workspace scope or produce conflicting outputs. <br>
Mitigation: Give each sub-agent clear, non-overlapping file scopes and review collected outputs before accepting changes. <br>
Risk: Unbounded or deeply nested spawning can increase runtime, cost, and coordination overhead. <br>
Mitigation: Use timeouts, keep orchestration one level deep, and reserve spawning for tasks where parallel work is justified. <br>
Risk: Final answers can become a loose concatenation of sub-agent results. <br>
Mitigation: Actively synthesize results by resolving conflicts, removing duplication, and adding the parent agent's context. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/indigas/claw-agent-spawner) <br>
- [README](README.md) <br>
- [Spawn Patterns](references/spawn-patterns.md) <br>
- [Model Selection](references/model-selection.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and optional JSON spawn plans] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Spawn plans can include subtask descriptions, dependencies, model recommendations, output formats, and synthesis instructions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact version history) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
