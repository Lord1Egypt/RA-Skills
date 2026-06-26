## Description: <br>
Get your AI agent a real US/Canada phone number in one API call. Make voice calls, send and receive SMS, and hold actual conversations via API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[modi2meet](https://clawhub.ai/user/modi2meet) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to provision and manage AgentPhone agents, phone numbers, SMS conversations, calls, contacts, and webhooks from an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can let an agent control real phone numbers, SMS, voice calls, OTP handling, and webhooks. <br>
Mitigation: Install only when this real-world communication authority is intended, and require explicit approval before sending texts, making calls, handling OTPs, or enabling webhooks. <br>
Risk: AgentPhone API keys grant account authority and can be misused if exposed. <br>
Mitigation: Use a dedicated API key stored in a secret manager or environment variable, send it only to api.agentphone.to, and rotate it if compromise is suspected. <br>
Risk: Buying or retaining phone numbers can create billing impact. <br>
Mitigation: Require explicit approval before buying numbers and monitor usage, number counts, and account limits. <br>
Risk: Releasing phone numbers and deleting agents or contacts are destructive actions. <br>
Mitigation: Require human confirmation before release or delete operations and preserve needed IDs or records before taking action. <br>
Risk: Webhook configuration can send communication events and context to external endpoints. <br>
Mitigation: Use only trusted HTTPS webhook destinations, verify ownership before enabling them, and review context limits and event handling. <br>


## Reference(s): <br>
- [AgentPhone homepage](https://agentphone.to) <br>
- [AgentPhone documentation](https://docs.agentphone.to) <br>
- [AgentPhone API base](https://api.agentphone.to) <br>
- [AgentPhone MCP Tools Reference](references/api-reference.md) <br>
- [ClawHub skill page](https://clawhub.ai/modi2meet/agentphone-ai) <br>
- [Publisher profile](https://clawhub.ai/user/modi2meet) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with API examples, shell commands, JSON snippets, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce API request examples and operational guidance for phone numbers, calls, SMS, contacts, account usage, and webhooks.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
