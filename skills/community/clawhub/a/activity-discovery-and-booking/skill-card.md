## Description:

Find things to do and places to eat in any city by natural-language search, with optional ticket booking and restaurant reservations through Outgoing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[outgoing](https://clawhub.ai/user/outgoing)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to discover restaurants, bars, concerts, museums, live events, outdoor activities, and other local outings, then optionally book tickets or make dining reservations after user confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Searches, location hints, and booking details may be shared with Outgoing.

Mitigation: Install and use the skill only when that data sharing is acceptable, and avoid sending unnecessary personal details.

Risk: Real ticket purchases, reservation deposits, or no-show holds can create charges or commitments.

Mitigation: Use dry-run tokens while testing and require explicit user confirmation before submitting any real purchase, deposit, or hold.

Risk: Venue details such as availability, accessibility, and pet policies may be incomplete or change outside the skill.

Mitigation: Report only what the API returns and ask the user to confirm important venue-specific requirements before relying on them.

## Reference(s):

- [Outgoing developer documentation](https://www.outgoing.world/developers)
- [Outgoing homepage](https://outgoing.world)
- [Outgoing API reference](https://www.outgoing.world/llms.txt)
- [Outgoing full API reference](https://www.outgoing.world/llms-full.txt)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, API calls, configuration, guidance]

**Output Format:** [Markdown with ranked activity recommendations, concise venue or event details, and inline curl examples or JSON payloads when making API calls.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include API-returned booking or reservation status, confirmation details, prices, availability, and image URLs; should not invent venues, prices, policies, or availability.]

## Skill Version(s):

0.2.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
