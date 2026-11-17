## Description:

Call EngageLab OTP REST APIs to send one-time passwords, verify codes, send custom template messages, manage OTP templates, configure callback webhooks, and support SMPP integration across SMS, WhatsApp, Email, and Voice channels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[devengagelab](https://clawhub.ai/user/devengagelab)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to generate API calls, code examples, shell commands, callback verification guidance, and configuration help for EngageLab OTP integrations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use long-lived EngageLab API credentials.

Mitigation: Store dev_key and dev_secret in environment variables or a secret manager, and do not paste dev_secret into chat.

Risk: Generated requests may send OTP or custom messages to real recipients.

Mitigation: Require explicit user confirmation before sending messages to production recipients.

Risk: Template management includes destructive delete actions.

Mitigation: Require explicit confirmation before deleting templates and verify the target template ID.

Risk: Callback payloads may contain recipient and delivery-status data.

Mitigation: Avoid logging callback payloads unless logs are redacted and access controlled.

Risk: Changing the API host could route credentials or recipient data to an unintended endpoint.

Mitigation: Restrict the API host to EngageLab's expected endpoint unless a trusted operator explicitly approves another host.

## Reference(s):

- [EngageLab OTP skill page](https://clawhub.ai/devengagelab/skills/engagelab-otp)
- [EngageLab OTP API endpoint](https://otp.api.engagelab.cc)
- [OTP Template API Reference](references/template-api.md)
- [OTP Callback Configuration Reference](references/callback-config.md)
- [EngageLab OTP API Error Codes](references/error-codes.md)
- [OTP SMPP Integration Guide](references/smpp-guide.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline code, shell commands, JSON examples, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include API request examples, authentication placeholders, template payloads, callback validation snippets, and error-handling guidance.]

## Skill Version(s):

1.0.1 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
