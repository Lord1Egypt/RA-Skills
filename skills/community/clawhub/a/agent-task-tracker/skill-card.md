## Description: <br>
Task Tracker maintains a concise local task state file so agents can resume requested work, background processes, progress, completions, and failures across session resets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rikouu](https://clawhub.ai/user/rikouu) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External developers and agents use this skill to keep a compact memory/tasks.md state snapshot of active tasks, background work, progress notes, and recent completions so work can resume after session resets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local task state file may retain sensitive task details across sessions. <br>
Mitigation: Review or clear memory/tasks.md for sensitive tasks, especially when notes include server names, commands, links, or error details. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/rikouu/agent-task-tracker) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Guidance] <br>
**Output Format:** [Markdown task state file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Maintains memory/tasks.md under 50 lines / 2KB, collapses completed tasks to one-line summaries, and prunes completed tasks older than 3 days.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
