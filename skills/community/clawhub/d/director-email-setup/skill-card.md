## Description:

Set up a dedicated email address for an agent using Resend, including sending, webhook-based receiving, inbox storage, and automated monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[di5cip1e](https://clawhub.ai/user/di5cip1e)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to give an agent a dedicated email identity, receive verification and notification messages, store inbound mail, and support owner-reviewed email workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive inbox data may be exposed through read or acknowledgement endpoints.

Mitigation: Require authentication on all inbox read and acknowledgement endpoints, store inbox data outside public paths, and apply retention limits.

Risk: Webhook spoofing could inject untrusted email content into the agent workflow.

Mitigation: Make Resend webhook signature verification mandatory before accepting inbound messages.

Risk: Email-driven automation can cause external actions without owner intent.

Mitigation: Require explicit owner approval before the agent replies, opens links, enters verification codes, or acts on email content.

Risk: A single broad Resend key can increase impact if credentials are exposed.

Mitigation: Use separate setup-time and runtime Resend keys and avoid exposing API keys or webhook secrets in logs or chat.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/di5cip1e/skills/director-email-setup)
- [Publisher profile](https://clawhub.ai/user/di5cip1e)
- [directorMail.js](references/directorMail.js)
- [inboundEmail.js](references/inboundEmail.js)
- [Resend API](https://api.resend.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with bash, JSON, and JavaScript snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces setup instructions and reference code for a Resend-backed agent inbox.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
