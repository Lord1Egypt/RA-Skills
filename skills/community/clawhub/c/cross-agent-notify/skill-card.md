## Description: <br>
Provides a standard cross-agent notification and handoff protocol for OpenClaw multi-agent setups using task files, inbox messages, session wakeups, and Feishu trace messages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sora-mury](https://clawhub.ai/user/sora-mury) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to delegate work, wake another agent for input or assistance, hand off completed work, and audit cross-agent collaboration consistency in OpenClaw multi-agent environments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Using the protocol may wake other agents and write shared task or inbox records in collaborative workspaces. <br>
Mitigation: Use it only where that coordination model and Feishu trace channel are expected, and review task and inbox updates before relying on them. <br>
Risk: Short Feishu group messages can be mistaken for the full task context. <br>
Mitigation: Keep full instructions in task files and inbox messages, and use group posts only as operational traces. <br>


## Reference(s): <br>
- [Cross-Agent Notification Protocol](references/PROTOCOL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Configuration] <br>
**Output Format:** [Markdown protocol guidance with task-file fields, inbox-message templates, session wakeup examples, and Feishu trace templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces operational coordination instructions; it does not include executable code or hidden install behavior.] <br>

## Skill Version(s): <br>
1.0.2 (source: release evidence and _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
