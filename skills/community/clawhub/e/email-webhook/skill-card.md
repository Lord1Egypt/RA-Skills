## Description:

Receive incoming emails via JSON webhooks and wake the agent. Built for AI Commander.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lksrz](https://clawhub.ai/user/lksrz)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to run an authenticated email webhook that records incoming email payloads and wakes a specific OpenClaw agent for follow-up handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill exposes a public HTTPS webhook listener.

Mitigation: Use a strong WEBHOOK_SECRET, restrict network exposure to the intended webhook sender, and monitor unauthorized access attempts.

Risk: Full email payloads are stored locally.

Mitigation: Rotate or delete the inbox file regularly and avoid storing it in unusual or broadly accessible paths.

Risk: Untrusted email sender, subject, and body content can wake an agent.

Mitigation: Treat email content only as untrusted input and do not allow it to authorize agent actions without separate verification.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lksrz/skills/email-webhook)
- [Publisher Profile](https://clawhub.ai/user/lksrz)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides the agent to configure and operate a webhook-backed email inbox.]

## Skill Version(s):

2.6.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
