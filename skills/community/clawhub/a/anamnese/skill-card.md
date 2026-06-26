## Description: <br>
Anamnese is a cloud-persistent memory and productivity skill that guides an agent to load user context, save useful facts, moments, notes, tasks, goals, and self-learning notes across conversations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[markoBel3](https://clawhub.ai/user/markoBel3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and their agents use Anamnese to maintain persistent personal context, tasks, goals, and assistant-specific learnings across sessions. It is intended for agents that should proactively capture meaningful user information and retrieve it in later conversations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Always-on capture can store broad personal and sensitive details in cloud-persistent memory. <br>
Mitigation: Enable the skill only when persistent memory is intended, confirm pause, review, delete, and export controls, and avoid storing health, financial, identity, location, relationship, or confidential work details unless explicitly chosen. <br>
Risk: Silent proactive saving may preserve information the user did not expect to keep long term. <br>
Mitigation: Search before saving, keep entries selective and useful for future sessions, and regularly review, update, or delete stored memories and notes. <br>


## Reference(s): <br>
- [Memory Management Reference](references/memory-management.md) <br>
- [Task Management Reference](references/task-management.md) <br>
- [Self-Review Reference](references/self-review.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API Calls, Text, Configuration] <br>
**Output Format:** [Markdown instructions with tool-call guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Prompts the agent to manage memories, notes, tasks, goals, and self-learning records through available memory tools.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
