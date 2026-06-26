## Description: <br>
Use this skill when an agent needs to register an OpenClaw identity with Crustacean Email Gateway, recover or reuse a bearer token, inspect mailbox state, manage inbox or outbox messages, configure forwarding, or send outbound email through the API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nycomar](https://clawhub.ai/user/nycomar) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to create and operate a Crustacean Email Gateway mailbox for an OpenClaw instance, including registration, token recovery, inbox and outbox review, forwarding configuration, and outbound email sending. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill saves and reuses a mailbox bearer token for authenticated email-gateway operations. <br>
Mitigation: Protect the configured token file like a password and install the skill only where the agent is expected to manage this mailbox. <br>
Risk: Outbound sending and forwarding can disclose email content or route future inbound mail to an external address. <br>
Mitigation: Review recipients and forwarding destinations before execution, especially because forwarding can persist without a destination verification flow. <br>
Risk: Mailbox registration, token recovery, and sending are subject to service rate limits and queued delivery behavior. <br>
Mitigation: Surface API error codes, messages, and retry-after values to the user, and check outbox status for queued messages. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nycomar/create-email-address) <br>
- [Crustacean Email Gateway API Reference](references/api.md) <br>
- [Usage Examples](references/examples.md) <br>
- [Crustacean Email Gateway API base](https://api.crustacean.email/api/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and terminal output, with optional JSON responses from the included scripts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write a local mailbox bearer token file and may perform authenticated email-gateway API calls.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
