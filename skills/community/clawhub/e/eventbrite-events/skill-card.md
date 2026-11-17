## Description:

Manage Eventbrite events, attendees, organizations, venues, orders, and ticketing data - powered by ClawLink.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hith3sh](https://clawhub.ai/user/hith3sh)

### License/Terms of Use:

MIT-0

## Use Case:

External users and operators use this skill to manage Eventbrite events, attendees, venues, orders, ticketing, promotions, and related organization data through ClawLink-connected OpenClaw tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawLink receives OAuth-based access that can read and change Eventbrite data for the connected account or organization.

Mitigation: Connect only Eventbrite accounts with the minimum roles needed and review the OAuth consent screen before authorizing access.

Risk: Some available operations can publish, cancel, delete, or materially change events, ticketing, webhooks, tracking, and buyer settings.

Mitigation: Require explicit review before high-impact Eventbrite changes and prefer lower-impact actions such as unpublishing when deletion or cancellation is not necessary.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/hith3sh/skills/eventbrite-events)
- [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=eventbrite-events)
- [ClawLink Eventbrite Connection](https://claw-link.dev/dashboard?add=eventbrite)

## Skill Output:

**Output Type(s):** [guidance, shell commands, code, API calls]

**Output Format:** [Markdown with inline shell and JavaScript examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces agent-facing setup steps, tool-selection guidance, and example ClawLink tool calls.]

## Skill Version(s):

1.0.5 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
