## Description: <br>
Orchestrate multi-agent teams with defined roles, task lifecycles, handoff protocols, and review workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lean-zhouchao](https://clawhub.ai/user/lean-zhouchao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to set up sustained teams of two or more specialized agents, route work through defined task states, and enforce handoffs and review gates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Shared agent workspaces can expose sensitive information if secrets are placed in shared directories. <br>
Mitigation: Keep shared directories free of secrets and provide only the workspace access each agent needs. <br>
Risk: Sustained multi-agent workflows can create uncontrolled cost, scheduling, or workspace-access scope if limits are not set. <br>
Mitigation: Define user-approved limits for spawning agents, scheduled work, budgets, and workspace access before deployment. <br>
Risk: Publisher identity requires attention because the security guidance notes a metadata mismatch. <br>
Mitigation: Verify the ClawHub publisher profile and release metadata before installing or delegating production work to this skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lean-zhouchao/agent-team-orchestration-bak) <br>
- [Team Setup](references/team-setup.md) <br>
- [Task Lifecycle](references/task-lifecycle.md) <br>
- [Communication](references/communication.md) <br>
- [Patterns](references/patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, configuration] <br>
**Output Format:** [Markdown guidance with task templates, workflow patterns, and setup conventions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only; no executable scripts or API calls.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
