## Description: <br>
A skill for main agents that need bounded delegation, safe parallel dispatch, and independent acceptance across multiple specialists. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cjke84](https://clawhub.ai/user/cjke84) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to decide when to keep work local, when to delegate bounded tasks to specialist agents, and how to verify and synthesize returned work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Delegated agents may receive more private or task-irrelevant context than needed. <br>
Mitigation: Keep each task contract narrow and share only the minimum context required for the delegated scope. <br>
Risk: Sub-agent output may be incomplete, out of scope, or inconsistent with other agent results. <br>
Mitigation: Require the main agent to verify boundary compliance, claimed checks, completeness, and cross-agent consistency before accepting the work. <br>
Risk: Community posts, account-affecting actions, or separately downloaded helper scripts can create external side effects. <br>
Mitigation: Require explicit review before public or account-affecting actions, and inspect any separately downloaded helper scripts before execution. <br>


## Reference(s): <br>
- [Agent Orchestrator Template](https://clawhub.ai/cjke84/agent-orchestrator-template) <br>
- [Publisher Profile](https://clawhub.ai/user/cjke84) <br>
- [Routing Configuration Template](references/routing-template.md) <br>
- [OpenClaw Local Playbook](references/openclaw-playbook.md) <br>
- [Task Contract Template](references/task-contract-template.md) <br>
- [Parallel Dispatch Rules](references/parallel-dispatch-rules.md) <br>
- [Acceptance Patterns](references/acceptance-patterns.md) <br>
- [Integration and Recovery Decisions](references/integration-and-recovery.md) <br>
- [Task Decomposition Template](references/task-decomposition-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, configuration, shell commands] <br>
**Output Format:** [Markdown guidance with structured task contracts, routing tables, checklists, and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces orchestration guidance for agent delegation, acceptance, recovery, and synthesis.] <br>

## Skill Version(s): <br>
0.1.1 (source: release evidence and manifest.toml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
