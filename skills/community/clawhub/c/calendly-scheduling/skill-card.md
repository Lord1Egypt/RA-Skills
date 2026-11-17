## Description:

Manage Calendly events, invitees, scheduling links, webhooks, and availability via the Calendly API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hith3sh](https://clawhub.ai/user/hith3sh)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to operate Calendly from an OpenClaw chat, including listing events and invitees, checking availability, creating scheduling links, managing webhooks, and handling event cancellations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install and allow an unpinned third-party plugin with ongoing access to a connected Calendly account.

Mitigation: Install only if the publisher and ClawLink are trusted, and prefer a pinned or otherwise verifiable plugin release when available.

Risk: OAuth-backed write actions can cancel events, modify organization membership, create webhooks, or delete Calendly data.

Mitigation: Preview write actions and confirm the target resource and intended effect before execution, especially for cancellations, organization changes, webhooks, and data deletion.

## Reference(s):

- [Calendly API Documentation](https://developer.calendly.com/)
- [Calendly Events API](https://developer.calendly.com/api-docs/evedefaultapi/scheduled-events)
- [Calendly Webhooks](https://developer.calendly.com/api-docs/webhook-subscriptions)
- [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=calendly-scheduling)
- [ClawLink Docs](https://docs.claw-link.dev/openclaw)
- [ClawLink Verification](https://claw-link.dev/verify)
- [ClawHub Skill Page](https://clawhub.ai/hith3sh/skills/calendly-scheduling)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, API calls]

**Output Format:** [Markdown guidance with shell command examples and JSON tool parameters]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include Calendly resource identifiers, scheduling links, webhook configuration details, and previews for write actions.]

## Skill Version(s):

1.0.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
