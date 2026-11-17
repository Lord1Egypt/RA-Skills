## Description:

Searches for businesses such as restaurants, salons, clinics, and hotels, then helps book, cancel, reschedule, or make merchant inquiries through AI phone calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[danielzhangreal](https://clawhub.ai/user/danielzhangreal)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to search local businesses, retrieve booking details, and initiate phone-based booking, cancellation, rescheduling, or merchant inquiry workflows through the LifeClaw API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can place, cancel, or reschedule real reservations through an external service.

Mitigation: Require explicit user confirmation of merchant, action, date, time, party size, name, contact details, cancellation, and reschedule details before initiating a phone call or updating a booking record.

Risk: The skill depends on a bearer token for authenticated LifeClaw API calls.

Mitigation: Store LIFECLAW_API_TOKEN outside prompts and logs, keep it scoped to the user, and revoke or rotate it if exposure is suspected.

Risk: User booking details and contact information are sent to the LifeClaw API and may be communicated to merchants.

Mitigation: Share only the minimum information needed for the requested booking or inquiry and confirm user consent before sending personal details.

## Reference(s):

- [LifeClaw Skill API Reference](references/api.md)
- [LifeClaw Homepage](https://lifeclaw.agentese.ai)
- [ClawHub Skill Page](https://clawhub.ai/danielzhangreal/skills/book-anything)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API Calls, Configuration]

**Output Format:** [Markdown guidance with REST API examples and JSON request or response shapes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires LIFECLAW_API_TOKEN for authenticated API calls.]

## Skill Version(s):

1.4.2 (source: release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
