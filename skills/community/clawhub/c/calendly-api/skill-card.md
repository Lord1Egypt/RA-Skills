## Description: <br>
Calendly API integration with managed OAuth for accessing event types, scheduled events, invitees, availability, booking workflows, and webhook management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to connect to Calendly through Maton, inspect scheduling data, check availability, book meetings, cancel scheduled events, and manage webhook subscriptions with user-approved API calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Maton API key and can access scheduling data through a connected Calendly account. <br>
Mitigation: Protect MATON_API_KEY, avoid exposing it in logs or shared prompts, and use only trusted runtime environments. <br>
Risk: Write operations can create invitees, cancel scheduled events, or create and delete webhook subscriptions. <br>
Mitigation: Require explicit user approval before any create, update, delete, booking, cancellation, or webhook operation, and confirm the target resource and intended effect. <br>
Risk: Multiple Calendly connections can cause requests to affect the wrong account. <br>
Mitigation: Verify the intended Calendly/Maton connection and include the Maton-Connection header when more than one connection exists. <br>


## Reference(s): <br>
- [ClawHub Calendly Skill Release](https://clawhub.ai/byungkyu/calendly-api) <br>
- [Calendly Developer Portal](https://developer.calendly.com/) <br>
- [Calendly API Reference](https://developer.calendly.com/api-docs) <br>
- [Calendly API Use Cases](https://developer.calendly.com/api-use-cases) <br>
- [Maton](https://maton.ai) <br>
- [Related ClawHub API Gateway Skill](https://clawhub.ai/byungkyu/api-gateway) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with HTTP endpoint descriptions and Python, JavaScript, and shell examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access, MATON_API_KEY, and a connected Calendly account through Maton.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
