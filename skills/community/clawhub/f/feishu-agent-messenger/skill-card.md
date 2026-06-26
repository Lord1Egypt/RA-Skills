## Description: <br>
Sends Feishu private or group chat messages from the current agent's configured Feishu application credentials so multi-agent workflows can report results under each agent's own bot identity. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pikaqiuyaya](https://clawhub.ai/user/pikaqiuyaya) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to let execution agents send Feishu status updates, task-completion notices, and direct messages without routing every reply through an orchestrator agent. It is intended for workspaces where agents are permitted to send external Feishu messages using local OpenClaw agent configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send external Feishu messages using local agent credentials. <br>
Mitigation: Install only in workspaces where agents are allowed to send Feishu messages, restrict access to ~/.openclaw/openclaw-*.json, and verify the agentId and recipient before sending. <br>
Risk: Task outputs or secrets could be sent to the wrong private or group chat. <br>
Mitigation: Avoid sending secrets or sensitive task outputs and confirm the open_id or chat_id before invoking the script. <br>
Risk: Automatic message.received hooks can create unscoped replies or message loops. <br>
Mitigation: Do not enable the hook unless trusted-sender allowlists, rate limits, and loop-prevention controls are added. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pikaqiuyaya/feishu-agent-messenger) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with bash, JSON, and JavaScript examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces Feishu text-message sending instructions and a shell script invocation pattern that uses agentId, recipient ID, message type, and message text.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata and artifact changelog, released 2026-03-20) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
