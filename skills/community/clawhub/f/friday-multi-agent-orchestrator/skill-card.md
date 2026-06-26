## Description: <br>
Designs multi-agent team roles, communication patterns, task distribution, conflict resolution, and priority management for agent teams. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[miio-jinglin](https://clawhub.ai/user/miio-jinglin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, solo founders, and operators use this skill to design role-specialized agent teams, choose coordination patterns, and set up task tracking and escalation rules. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Shared directories can expose task data or coordination state to agents that do not need it. <br>
Mitigation: Decide which agents can access each shared directory before using the skill operationally. <br>
Risk: Agent teams may prepare or request sensitive actions such as deployments, publishing, finance, or account changes. <br>
Mitigation: Require human approval for sensitive actions and keep strategic decisions human-in-the-loop. <br>
Risk: Heartbeat or cron jobs can continue running without clear ownership or review. <br>
Mitigation: Track scheduled monitoring jobs, owners, and review cadence before enabling them. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/miio-jinglin/friday-multi-agent-orchestrator) <br>
- [Skill definition](SKILL.md) <br>
- [Team Roles](references/team-roles.md) <br>
- [Communication Patterns](references/communication-patterns.md) <br>
- [Task Management](references/task-management.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with templates, tables, and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only; no hidden executable behavior reported by security evidence.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
