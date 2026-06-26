## Description: <br>
Self-driving agent workflow with heartbeat-driven task execution, day/night progress reports, and long-term memory consolidation. Integrates with todo-management for task tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[15228947433](https://clawhub.ai/user/15228947433) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to configure an OpenClaw sub-agent that autonomously selects todo items, records work, sends periodic progress reports, and maintains long-term memory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent autonomous execution can continue changing local project state and agent memory with weak stop and approval boundaries. <br>
Mitigation: Use a narrow workspace, review identity and memory files before enabling heartbeat execution, define explicit stop conditions, and require confirmation for commits, deployments, external resources, credential use, and broad file changes. <br>
Risk: Heartbeat templates encourage the agent to keep working when goals are not yet met. <br>
Mitigation: Set bounded objectives and heartbeat intervals, monitor todo state and memory logs, and disable heartbeat execution when the agent reaches its intended scope. <br>
Risk: The initialization script creates workspace state and copies the todo-management skill into the target workspace. <br>
Mitigation: Run initialization only against the intended workspace path and review the resulting skills, memory, and report-state files before use. <br>


## Reference(s): <br>
- [Example setup](references/example-setup.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with inline bash commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes heartbeat, reporting, memory, workspace initialization, and todo-management setup guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and auto changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
