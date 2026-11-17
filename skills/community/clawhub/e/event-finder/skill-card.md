## Description:

Find public Facebook events by keyword or city, view event details, and list events hosted by a page without a Facebook account or API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hith3sh](https://clawhub.ai/user/hith3sh)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users can find public events for weekend planning, meetups, conferences, and event tracking, then review event times, venues, descriptions, and hosts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Event lookups require a third-party ClawLink plugin and one-time pairing approval.

Mitigation: Review the plugin before installing and approve pairing only when the user requests it.

Risk: Each lookup consumes ClawLink credit; large batches can incur charges.

Mitigation: Check current tool prices and get explicit approval before larger paid batches.

Risk: The connector is limited to public Facebook event information.

Mitigation: Use it only for public event data, not private accounts or actions that modify data.

## Reference(s):

- [Event Finder on ClawHub](https://clawhub.ai/hith3sh/skills/event-finder)
- [Publisher profile](https://clawhub.ai/user/hith3sh)
- [ClawLink OpenClaw documentation](https://docs.claw-link.dev/openclaw)
- [ClawLink pricing](https://claw-link.dev/pricing?utm_source=clawhub&utm_medium=referral&utm_content=event-finder)
- [Verify the ClawLink plugin](https://claw-link.dev/verify)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Conversational summaries and event lists in Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Public event results may include dates, venues, descriptions, hosts, and attendance counts; lookups consume ClawLink credit.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
