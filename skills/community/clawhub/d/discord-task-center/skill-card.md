## Description: <br>
Handles Discord task-center forums by creating task posts, archiving tasks by tag, and respecting model tags for conversations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nannyu](https://clawhub.ai/user/nannyu) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to manage Discord forum threads as task-center items, including creating task threads, applying task labels, and archiving current tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad task-management trigger phrases can accidentally create or archive Discord forum threads. <br>
Mitigation: Use a minimally privileged Discord bot, restrict it to the intended server and forum, and require confirmation or explicit command phrasing before creating or archiving tasks. <br>
Risk: Forum task operations can change Discord thread tags and task visibility. <br>
Mitigation: Review the target thread and intended tag changes before applying create, archive, or channel-management actions. <br>


## Reference(s): <br>
- [Discord Task Center API Reference](reference.md) <br>
- [ClawHub Discord Skill](https://clawhub.ai/steipete/discord) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline commands and Discord task-operation instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a configured Discord forum task-center integration and compatible Discord skill.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and clawhub.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
