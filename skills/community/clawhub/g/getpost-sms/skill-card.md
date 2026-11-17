## Description:

Send and receive SMS messages via API using shared or dedicated numbers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dommholland](https://clawhub.ai/user/dommholland)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agent builders use this skill to integrate GetPost SMS signup, sending, inbox, dedicated-number provisioning, and webhook workflows into an agent or application.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Phone numbers, SMS message bodies, webhook payloads, and GetPost API keys may contain sensitive data.

Mitigation: Store API keys in a secret manager, limit logging of message contents and phone numbers, and protect webhook endpoints.

Risk: SMS sending can create consent, telecom compliance, and billing exposure.

Mitigation: Send messages only to recipients who have consented, review provider terms and regional messaging rules, and monitor credit usage.

## Reference(s):

- [GetPost SMS API Documentation](https://getpost.dev/docs/api-reference#sms)
- [ClawHub Skill Page](https://clawhub.ai/dommholland/skills/getpost-sms)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes API endpoint examples and bearer-token authentication patterns.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
