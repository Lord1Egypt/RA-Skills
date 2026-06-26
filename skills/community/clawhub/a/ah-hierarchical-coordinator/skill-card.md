## Description: <br>
Hierarchical Coordinator helps agents decompose complex projects into multi-level task hierarchies, delegate work to specialized agents, and synthesize results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mtsatryan](https://clawhub.ai/user/mtsatryan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineering leads, and agent operators use this skill to plan complex software or enterprise projects by assessing complexity, assigning hierarchical agent responsibilities, tracking dependencies, and aggregating results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Delegated agents may receive broader project context than needed for a subtask. <br>
Mitigation: Scope each delegated agent to the minimum context needed and require escalation for cross-domain changes. <br>
Risk: The skill can coordinate work that involves purchases, crypto/payment activity, deployments, or broad code changes. <br>
Mitigation: Require explicit human approval before those actions and review generated plans before execution. <br>
Risk: Hierarchical decomposition may propagate incorrect assumptions from parent tasks into subtasks. <br>
Mitigation: Use sync points, quality gates, and final synthesis review to validate dependencies and outputs before implementation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mtsatryan/ah-hierarchical-coordinator) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/mtsatryan) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown planning templates, task breakdowns, coordination plans, progress dashboards, and synthesis summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only output; review generated plans before acting on delegated work.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
