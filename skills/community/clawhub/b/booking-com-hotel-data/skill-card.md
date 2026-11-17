## Description:

Search Booking.com hotels through Scavio for live stay prices, property details, room rates, and guest reviews.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scavio-ai](https://clawhub.ai/user/scavio-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Travel planners, travelers, and developers use this skill to compare hotel prices for a stay, inspect a property's rooms and policies, and review guest feedback.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search details, including dates, guest counts, children's ages, and selected property URLs, are sent to the third-party Scavio service.

Mitigation: Share only necessary travel details and confirm the user is comfortable with third-party processing.

Risk: The Scavio API key could be exposed if stored in source control or shared output.

Mitigation: Keep the API key in a secret store or environment variable and never include it in source control or responses.

Risk: API calls consume credits, including empty results, while live prices and availability can change before booking.

Mitigation: Avoid unnecessary requests, track credit usage, and verify dated prices and availability at the linked property before booking.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/scavio-ai/skills/booking-com-hotel-data)
- [Scavio Booking search documentation](https://scavio.dev/docs/booking-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=booking-com-hotel-data)
- [Scavio rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=booking-com-hotel-data)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown with hotel results, prices, review summaries, and property links; optional JSON excerpts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Quotes should identify the stay dates, currency, price basis, and time checked.]

## Skill Version(s):

1.0.5 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
