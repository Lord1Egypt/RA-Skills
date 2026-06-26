## Description: <br>
Self-driving agent workflow with heartbeat-driven task execution, day/night progress reports, and long-term memory consolidation. Integrates with todo-management for task tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[edoserbia](https://clawhub.ai/user/edoserbia) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to configure an OpenClaw agent for recurring autonomous task execution, progress reporting, todo tracking, and memory maintenance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recurring autonomous write and memory-edit authority can exceed intended boundaries. <br>
Mitigation: Install the skill only in a dedicated, bounded workspace with clear stop conditions before enabling heartbeat automation. <br>
Risk: Automated memory cleanup, git commits, external tool use, or high-impact file changes can affect project state. <br>
Mitigation: Require human review before memory cleanup, git commits, external tool use, or high-impact file changes. <br>
Risk: The workflow copies or depends on the todo-management skill. <br>
Mitigation: Verify the copied todo-management skill source before enabling the autopilot workflow. <br>


## Reference(s): <br>
- [Agent Autopilot on ClawHub](https://clawhub.ai/edoserbia/agent-autopilot) <br>
- [Example Setup](references/example-setup.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash commands, workflow templates, and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces heartbeat, memory, reporting, and todo-management setup guidance for an agent workspace.] <br>

## Skill Version(s): <br>
1.4.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
