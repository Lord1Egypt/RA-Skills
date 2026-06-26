## Description: <br>
API-first email platform designed for AI agents to create and manage dedicated email inboxes, send and receive emails programmatically, and handle email-based workflows with webhooks and real-time events. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Liguang00806](https://clawhub.ai/user/Liguang00806) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to connect agents to AgentMail inboxes, send and receive messages, and configure webhook-driven email workflows. It is suited for agent identity, customer support automation, notifications, document-processing workflows, and other email-based operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Webhook examples can expose full email contents to third-party endpoints or logs. <br>
Mitigation: Use trusted webhook endpoints, avoid logging full payloads, and keep sensitive message content out of forwarding or debugging flows. <br>
Risk: Incoming email can be used as untrusted input that attempts to direct agent behavior. <br>
Mitigation: Restrict senders with an allowlist, isolate review sessions for untrusted mail, and require confirmation before acting on email instructions. <br>
Risk: Email automation can send, forward, or retain messages beyond the user's intent. <br>
Mitigation: Start with test inboxes, scope the API key, require confirmation before sending or forwarding, and clean up inboxes and webhooks after use. <br>


## Reference(s): <br>
- [AgentMail API Reference](references/API.md) <br>
- [AgentMail Webhooks Guide](references/WEBHOOKS.md) <br>
- [AgentMail Usage Examples](references/EXAMPLES.md) <br>
- [AgentMail Console](https://console.agentmail.to) <br>
- [AgentMail API Base URL](https://api.agentmail.to/v0) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with Python, shell, HTTP, TypeScript, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Examples and helper scripts assume an AgentMail account and an AGENTMAIL_API_KEY environment variable.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
