## Description: <br>
Designs multi-agent system architectures with agent roles, communication protocols, memory strategy, escalation structure, operational schedules, and risk maps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[filipbl4gojevic](https://clawhub.ai/user/filipbl4gojevic) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to turn a workflow or goal into a structured multi-agent architecture with oversight points, memory boundaries, escalation rules, schedules, and risks before implementation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated swarm plans may be used to configure agents that can affect real systems. <br>
Mitigation: Keep human approval gates before irreversible actions, test plans in a sandbox, and require rollback paths before production use. <br>
Risk: Overbroad agent roles or shared memory can create scope creep, stale state, or coordination failures. <br>
Mitigation: Apply least-privilege access, assign a single owner for shared state, use explicit communication protocols, and review mandates before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/filipbl4gojevic/agent-swarm-planner) <br>
- [Agent Swarm Failure Patterns](references/failure-patterns.md) <br>
- [Swarm Architecture Template](templates/swarm-architecture-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown architecture document with tables, checklists, and structured sections] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes agent roster, communication architecture, shared memory design, escalation structure, operational schedule, risk map, open questions, and assumptions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
