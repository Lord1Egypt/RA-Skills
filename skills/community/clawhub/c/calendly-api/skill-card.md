## Description:

Helps agents access Calendly scheduling data and manage approved scheduling workflows through a connected Maton account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[byungkyu](https://clawhub.ai/user/byungkyu)

### License/Terms of Use:

MIT-0

## Use Case:

Users and developers can ask an agent to review Calendly event types, meetings, invitees, and availability, or to set up approved bookings, webhooks, and scheduling automations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Calendly access can expose invitee details and meeting links.

Mitigation: Confirm the intended account and requested data, use least-privilege access, and approve writes separately.

Risk: Webhooks, triggers, and hosted functions may persistently forward scheduling information.

Mitigation: Before approval, review the exact destination URL, data fields, and how long the automation will remain active.

## Reference(s):

- [ClawHub Calendly skill](https://clawhub.ai/byungkyu/skills/calendly-api)
- [Maton](https://maton.ai)
- [Calendly API documentation](https://developer.calendly.com/api-docs)
- [Maton CLI manual](https://cli.maton.ai/manual)
- [Calendly trigger reference](artifact/references/calendly/triggers.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, JSON examples]

**Output Format:** [Markdown with shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read/list operations by default; account connections, writes, and automation require user approval.]

## Skill Version(s):

1.2.7 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
