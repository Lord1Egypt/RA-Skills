## Description: <br>
Control spawned Feishu background tasks with concise natural-language or slash-command workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wd041216-bit](https://clawhub.ai/user/wd041216-bit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Feishu chat users use this skill to inspect active background tasks in the current chat, resolve ambiguous task targets, and stop one task, all tasks, or the current run. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A broad stop or kill request could cancel active background work in the current Feishu chat. <br>
Mitigation: Use specific task numbers or labels when multiple tasks are running, and ask the user to disambiguate when the requested task target is unclear. <br>
Risk: Task-control replies could expose internal session details if raw tool output is repeated to the user. <br>
Mitigation: Return only concise, human-readable task status or stop results, and do not expose raw JSON, session ids, or command payloads. <br>


## Reference(s): <br>
- [Feishu Task Control on ClawHub](https://clawhub.ai/wd041216-bit/feishu-task-control) <br>
- [OpenClaw Commands](https://docs.openclaw.ai/commands) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands] <br>
**Output Format:** [Markdown with concise user-facing status or task-control command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Chinese or English task status replies depending on the Feishu chat context.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
