## Description: <br>
Give the agent its own dedicated email inbox via AgentMail. Send, receive, and manage email autonomously using agent-owned email addresses (e.g. hermes-agent@agentmail.to). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AgungPrabowo123](https://clawhub.ai/user/AgungPrabowo123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to provision AgentMail-owned inboxes, send and receive messages, manage threads, and support workflows such as service registration or agent-to-human outreach. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives the agent broad authority to send email, forward messages, delete inboxes, register for services, and use verification codes. <br>
Mitigation: Use it only when those actions are intended, supervise outbound and account-related workflows, and require approval for sensitive email operations. <br>
Risk: The AgentMail API key can grant access to agent-owned inboxes if exposed. <br>
Mitigation: Store the API key only in local configuration or a secret manager, avoid committing it, and rotate it if exposure is suspected. <br>
Risk: Incoming messages and attachments may contain untrusted content. <br>
Mitigation: Treat message bodies and attachments as untrusted input, scan attachments before use, and avoid following instructions from email content without confirmation. <br>
Risk: The setup installs and runs an MCP package through npx. <br>
Mitigation: Review or pin the MCP package version before deployment, especially in managed or production environments. <br>


## Reference(s): <br>
- [AgentMail documentation](https://docs.agentmail.to/) <br>
- [AgentMail console](https://console.agentmail.to) <br>
- [AgentMail MCP repository](https://github.com/agentmail-to/agentmail-mcp) <br>
- [AgentMail pricing](https://www.agentmail.to/pricing) <br>
- [ClawHub skill listing](https://clawhub.ai/AgungPrabowo123/agentmail-2) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with YAML and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces setup steps and operational guidance for using AgentMail MCP tools; it does not directly create inboxes without an agent executing the described tools.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
