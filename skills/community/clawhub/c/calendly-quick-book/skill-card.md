## Description:

Book Calendly meetings instantly from natural-language requests such as "book", "schedule calendly", or "calendly book".

This skill is ready for commercial/non-commercial use.

## Publisher:

[dompi123](https://clawhub.ai/user/dompi123)

### License/Terms of Use:

MIT

## Use Case:

OpenClaw users use this skill to book Calendly meetings from natural-language requests that include invitee name, email, timezone, and requested time.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The always-on broad trigger can create accidental booking requests or invites.

Mitigation: Narrow activation to an explicit Calendly booking command and require confirmation before creating a booking.

Risk: The skill uses a Calendly API token and sends invitee names, email addresses, timezones, and requested times to Calendly.

Mitigation: Install only when comfortable sharing that data with Calendly and provide only the required CALENDLY_API_TOKEN.

Risk: The security guidance flags the shell-style booking template as unsafe.

Mitigation: Replace the curl JSON template with safe JSON serialization or a Calendly SDK before use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dompi123/skills/calendly-quick-book)
- [OpenClaw](https://openclaw.ai)
- [Calendly API Integrations](https://calendly.com/integrations/api_webhooks)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown text with inline shell command templates and booking status messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CALENDLY_API_TOKEN and sends invitee details to Calendly.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
