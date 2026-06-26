## Description: <br>
Enables the Agentic Workflow (Kanban + Heartbeat + QA Subagent). Use this when instructed to set up a continuous, asynchronous task system for any agent. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Mashirops](https://clawhub.ai/user/Mashirops) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to set up a task board, heartbeat executor, and QA-checker loop so an OpenClaw agent can continue work asynchronously and verify outputs before notifying the user. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sets up an autonomous heartbeat-driven workflow that can keep changing workspace files with limited user visibility. <br>
Mitigation: Install it only when that behavior is intended, confirm which files it creates or edits, define how to pause or disable it, and monitor activity between user messages. <br>
Risk: The workflow can stay silent while work is in progress, so operators may miss intermediate actions until a task reaches DONE or BLOCKED. <br>
Mitigation: Review TASK_BOARD.yaml and HEARTBEAT.md before use and require clear DONE or BLOCKED notifications for completed or stalled work. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Mashirops/agentic-workflow) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown guidance with YAML and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or updates workspace task-management files when applied.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
