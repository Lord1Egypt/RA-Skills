## Description: <br>
Give your OpenClaw agent its own email inbox. Use AgentSend to create inboxes, send and receive email, inspect threads, and register webhooks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luv005](https://clawhub.ai/user/luv005) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to give an agent a managed email inbox, send and receive messages, inspect email threads, and register email event webhooks through AgentSend. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill delegates email inbox access and credential handling to an external AgentSend MCP runtime. <br>
Mitigation: Use a dedicated API key or sandbox account, and delete or secure ~/.agentsend/credentials.json when the retained sandbox credential is no longer needed. <br>
Risk: Outbound email can be sent from an agent-managed inbox. <br>
Mitigation: Confirm the sender inbox, recipients, subject, and body before sending messages. <br>
Risk: Webhook registration can send email events to external URLs. <br>
Mitigation: Register webhooks only for URLs the user controls. <br>


## Reference(s): <br>
- [AgentSend Skill Documentation](https://agentsend.io/skill) <br>
- [ClawHub Skill Page](https://clawhub.ai/luv005/agentsend-email) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with MCP tool usage, configuration notes, and email or thread data returned by AgentSend.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May involve inbox addresses, email bodies, message headers, attachment metadata, webhook URLs, and credential setup details.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
