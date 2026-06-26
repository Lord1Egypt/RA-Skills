## Description: <br>
Defines the collaboration protocol between main session and sub-agent sessions for executing heavy tasks such as analysis, search, and writing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[slientrain-new](https://clawhub.ai/user/slientrain-new) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to delegate long-running or high-context tasks to isolated sub-agent sessions, track progress with task.md checklists, recover from crashes, and run lightweight retrospectives after completion. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Delegated sessions may create persistent task logs and step files that contain sensitive task content. <br>
Mitigation: Use isolated workspaces for delegated tasks and delete or redact task logs and step files before sharing or retaining them. <br>
Risk: The workflow can send completed results to external messaging channels when notification is enabled. <br>
Mitigation: Disable external notification by default and require explicit confirmation before any result is sent outside the local session. <br>
Risk: Sub-agents may operate with under-scoped authority when handling broad delegated tasks. <br>
Mitigation: Pass narrowly scoped tasks, limit available tools and channels to what the task requires, and review completed outputs before relying on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/slientrain-new/claw-subagent-orchestrator) <br>
- [Sub-agent collaboration protocol](docs/protocol.md) <br>
- [Task checklist template](templates/task.md) <br>
- [Retrospective template](templates/task-retro.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, configuration] <br>
**Output Format:** [Markdown instructions with task templates and structured checklist conventions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create persistent task logs, step notes, and retrospective files in the delegated workspace.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
