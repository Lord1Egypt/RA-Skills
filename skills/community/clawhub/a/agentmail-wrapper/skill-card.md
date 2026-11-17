## Description:

Send, track, schedule, and manage email delivery across SMTP, SendGrid, Mailgun, AWS SES, and Gmail OAuth providers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shepherd217](https://clawhub.ai/user/shepherd217)

### License/Terms of Use:

MIT

## Use Case:

Developers and automation builders use this skill to integrate transactional email, campaign sends, scheduled sequences, delivery tracking, unsubscribe handling, and compliance reporting into agent workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Email sending, batch delivery, and open/click tracking can create consent, compliance, and abuse risk if enabled without clear authorization.

Mitigation: Confirm the legal basis for recipients and tracking before use; require unsubscribe handling, rate limits, bounce handling, and approval for campaign or batch sends.

Risk: The security evidence flags unaudited external packages and incomplete guardrails.

Mitigation: Install first in a test or least-privilege environment and require verified, pinned package sources before production use.

Risk: Provider API keys and Gmail refresh tokens can authorize email access or sending if exposed.

Mitigation: Store credentials in a protected secrets manager, grant minimal scopes, rotate secrets periodically, and avoid committing tokens or keys.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/shepherd217/skills/agentmail-wrapper)
- [Declared Documentation](https://docs.midas-skills.com/agentmail-wrapper)
- [Declared Repository](https://github.com/midas-skills/agentmail-wrapper)

## Skill Output:

**Output Type(s):** [code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JavaScript and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include provider configuration, email-send examples, tracking options, and operational compliance guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata, package.json, SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
