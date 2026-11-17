## Description:

Searches, compares, books, and fixes flights across fares, connections, baggage, seats, miles, delays, passenger rights, travel documents, passenger needs, corporate policy, and flight-data APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to plan, compare, book, monitor, change, and troubleshoot flights, including fare rules, award tickets, baggage, disruptions, refunds, travel documents, passenger needs, and corporate travel constraints. It can also guide developers who are building flight-search, pricing, tracking, or booking workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks for broad local travel, booking, contact, finance, project, and profile access.

Mitigation: Install only when a persistent local flight assistant is intended, and review the configured folders before use.

Risk: The skill can keep sensitive travel plans, locators, loyalty data, companion details, claims, and card-fee metadata in plain local notes.

Mitigation: Back up and protect those local files, and avoid storing passwords, card numbers, passport numbers, bank details, boarding-pass barcodes, or programme PINs.

Risk: The skill writes sensitive records without a confirmation gate, including possible deletions or shared finance and contact updates.

Mitigation: Review writes and deletions, especially shared booking, finance, contact, and project updates.

## Reference(s):

- [Flight skill on ClawHub](https://clawhub.ai/ivangdavila/skills/flight)
- [Flight homepage](https://clawic.com/skills/flight)
- [Clawic](https://clawic.com)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown and plain-text travel guidance, with structured tables or local-note entries when useful.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce durable local travel-memory updates when the user asks or when the skill records flights, prices, deadlines, loyalty data, claims, vouchers, or reusable procedures.]

## Skill Version(s):

1.0.3 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
