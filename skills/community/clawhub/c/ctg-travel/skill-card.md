## Description:

Ctg Travel helps agents guide users through CTG travel searches, bookings, cancellations, and refunds for flights, hotels, trains, and attraction tickets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ctg-travel](https://clawhub.ai/user/ctg-travel)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-support agents use this skill to search, book, cancel, and refund CTG flights, hotels, train tickets, and attraction tickets through guided conversations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use a CTG API key to access passenger and order information.

Mitigation: Provide CTG_API_KEY through a secure environment or secret manager and avoid storing credentials in chat or local config when a safer secret path is available.

Risk: The skill can create, cancel, or refund travel orders, which may affect bookings and money.

Mitigation: Require explicit final user confirmation after showing the selected itinerary, passenger or visitor details, price, refund amount, and fees before submitting an order, cancellation, or refund.

Risk: Travel workflows may expose personal passenger, guest, visitor, order, and contact details.

Mitigation: Show only the details needed for the current user decision and avoid including raw API responses or unnecessary identifiers in user-facing output.

## Reference(s):

- [ClawHub Ctg Travel skill page](https://clawhub.ai/ctg-travel/skills/ctg-travel)
- [CTG OpenClaw integration guide](https://pro-m.ourtour.com/new-journey/static-page/openClawGuide)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Plain-language responses and Markdown with shell commands and JSON arguments for CTG travel operations.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CTG_API_KEY; booking, cancellation, and refund flows should receive explicit user confirmation before submission.]

## Skill Version(s):

1.0.5 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
