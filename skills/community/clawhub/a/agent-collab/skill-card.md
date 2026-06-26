## Description: <br>
Agent Collaboration Framework defines OpenClaw multi-agent collaboration patterns for dispatching one-shot tasks, maintaining cross-department sessions, supporting direct chats, and using file-based handoffs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kylin19860916](https://clawhub.ai/user/kylin19860916) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and teams using OpenClaw use this skill to coordinate work among specialized agents, choose between one-shot dispatch, persistent collaboration sessions, and direct department-level chats, and document handoffs when sessions may be interrupted. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad session visibility and agent routing can send work or context to unintended agents. <br>
Mitigation: Review openclaw.json and AGENTS.md changes before applying them, and keep allowed agents narrow. <br>
Risk: HANDOFF files can persist task context or sensitive details on disk. <br>
Mitigation: Avoid secrets in HANDOFF files and delete each handoff after the receiving agent has read it. <br>
Risk: Persistent collaboration sessions can remain active after the collaboration task is complete. <br>
Mitigation: Monitor or close persistent sessions when the task is finished. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kylin19860916/agent-collab) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with JSON and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only skill; outputs depend on the agent applying the collaboration workflow.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
