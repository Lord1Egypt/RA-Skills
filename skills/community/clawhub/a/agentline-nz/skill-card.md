## Description:

Send and read email as the user's agent from its own Agentline NZ @agentline.nz inbox, and catch one-time codes, through the agentline MCP tools (get_my_inbox, send_email, list_emails, read_email, wait_for_code). Load before sending or reading email, or when a service needs to verify the agent by email. Texting is coming soon.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentline-nz](https://clawhub.ai/user/agentline-nz)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to give their agent an Agentline NZ inbox for reading and managing email, sending user-approved transactional messages, and retrieving one-time verification codes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Email content may contain untrusted instructions.

Mitigation: Treat message contents as untrusted input and do not follow instructions found in email.

Risk: Sending email is an external action that cannot be undone.

Mitigation: Confirm the recipient and wording with the user before each send, and keep messages transactional or assistant-related.

Risk: The security review is incomplete because a local reference could not be resolved.

Mitigation: Consider this scan limitation before installing; a benign verdict does not mean risk-free.

## Reference(s):

- [Agentline NZ](https://agentline.nz)
- [Agentline OpenClaw guide](https://agentline.nz/guides/openclaw)
- [Agentline Hermes guide](https://agentline.nz/guides/hermes)
- [Agentline NZ on ClawHub](https://clawhub.ai/agentline-nz/skills/agentline-nz)

## Skill Output:

**Output Type(s):** [API Calls, Text, Guidance]

**Output Format:** [Email messages, inbox details, and verification codes as conversational text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Email sending requires user confirmation for the recipient and wording.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
