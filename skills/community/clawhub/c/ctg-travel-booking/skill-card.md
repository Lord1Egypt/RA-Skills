## Description:

Ctg Travel Booking is an expired CTG Travel Open Platform assistant for guided lookup, booking, cancellation, and refund workflows across flights, hotels, train tickets, and attraction tickets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaosai](https://clawhub.ai/user/xiaosai)

### License/Terms of Use:

MIT-0

## Use Case:

External travelers and travel-service agents use this skill to collect trip details, query options, prepare orders, and handle cancellations or refunds for CTG Travel resources. Because the release is expired, users should prefer the newer linked version when available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release is expired and no longer maintained.

Mitigation: Prefer the newer CTG Travel skill linked by the release before installing or using this version.

Risk: The skill handles API keys, passenger identity details, contact information, and order data.

Mitigation: Configure only a trusted HTTPS CTG Travel endpoint and share identity or contact data only when needed for the requested booking or refund.

Risk: Booking, cancellation, and refund actions can change orders or move money if submitted ambiguously.

Mitigation: Require a clear final summary and explicit user confirmation before any booking, cancellation, or refund submission.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/xiaosai/skills/ctg-travel-booking)
- [Current CTG Travel Skill](https://clawhub.ai/ctg-travel/ctg-travel)
- [CTG Travel Skill Access Guide](https://pro-m.ourtour.com/new-journey/static-page/openClawGuide)
- [Skill Definition](artifact/SKILL.md)
- [API Configuration](artifact/config/ctgConfig.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON request parameters]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May trigger authenticated POST requests to the configured CTG Travel endpoint; booking, cancellation, and refund actions require final user confirmation.]

## Skill Version(s):

0.2.5 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
