## Description: <br>
Integrates the AgentMail API so agents can create and manage dedicated inboxes, send and receive email, and handle webhook-driven email workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[synesthesia-wav](https://clawhub.ai/user/synesthesia-wav) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to add AgentMail-based email identity, inbox management, sending, receiving, webhook handling, and common email automation workflows to agent projects. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses an AgentMail API key with permissions to send email, manage inboxes, and register webhooks. <br>
Mitigation: Use a scoped or dedicated key when available, restrict access to trusted deployments, and require human approval for outbound replies or forwarding. <br>
Risk: Incoming email and webhook payloads can contain prompt injection or unsafe instructions. <br>
Mitigation: Use sender allowlists, treat message content as untrusted context, filter suspicious content, and queue risky messages for human review. <br>
Risk: Received attachments may be untrusted and can be saved to local files by helper scripts or documented workflows. <br>
Mitigation: Do not automatically process attachments from untrusted senders; sanitize filenames, scan files, and limit download locations before use. <br>


## Reference(s): <br>
- [AgentMail API Reference](references/API.md) <br>
- [Webhook Setup and Security](references/WEBHOOKS.md) <br>
- [AgentMail Common Patterns](references/patterns.md) <br>
- [AgentMail Examples](references/EXAMPLES.md) <br>
- [AgentMail Console](https://console.agentmail.to) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python examples, shell commands, and configuration steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include AgentMail API calls and local helper script usage that require an AGENTMAIL_API_KEY.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
