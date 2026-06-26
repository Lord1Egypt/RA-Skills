## Description: <br>
Send and receive SMS messages via API. Shared or dedicated numbers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dommholland](https://clawhub.ai/user/dommholland) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to connect an agent to the GetPost SMS API for sending texts, reading an inbox, provisioning dedicated numbers, and registering SMS webhooks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: An agent with API credentials can send SMS messages, read inbox contents, provision numbers, or register webhooks. <br>
Mitigation: Keep the API key private and require explicit approval for recipients, message content, number provisioning, inbox access, and webhook registration. <br>
Risk: Phone numbers and SMS contents can contain sensitive data. <br>
Mitigation: Treat phone numbers and SMS messages as sensitive data, limit retention and logging, and use the skill only with appropriate consent. <br>


## Reference(s): <br>
- [GetPost SMS API documentation](https://getpost.dev/docs/api-reference#sms) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, API calls, configuration] <br>
**Output Format:** [Markdown with curl command examples and endpoint guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a GetPost Bearer API key; actions may send SMS messages, read inbox contents, provision numbers, or register webhooks.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
