## Description: <br>
Capability Pipeline OS helps agents decompose tasks into executable capability units and orchestrate them through structured pipelines. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangjiaocheng](https://clawhub.ai/user/wangjiaocheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, planners, and agent users use this skill to turn broad or multi-step tasks into capability units and ordered pipelines with explicit dependencies, autonomy levels, guard checks, and output handoffs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The framework uses broad planning and task-orchestration language that could lead an agent to over-assume autonomy. <br>
Mitigation: Require explicit confirmation before edits, code execution, external submissions, transactions, deployments, or other irreversible steps. <br>
Risk: Pipeline outputs can appear authoritative even when they are planning structures rather than verified facts. <br>
Mitigation: Treat the skill as a structuring aid and verify domain facts, constraints, and safety checks before acting. <br>


## Reference(s): <br>
- [Capability Pipeline OS on ClawHub](https://clawhub.ai/wangjiaocheng/capability-pipeline-os) <br>
- [Publisher profile: wangjiaocheng](https://clawhub.ai/user/wangjiaocheng) <br>
- [Capability Pipeline OS reference](references/capability-pipeline-os.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, configuration] <br>
**Output Format:** [Markdown task decomposition with tables, pipeline structures, and step-by-step guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces planning structures and orchestration guidance; does not execute tools or make irreversible changes by itself.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
