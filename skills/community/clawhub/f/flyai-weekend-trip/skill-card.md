## Description:

Plans three 2-day, 1-night weekend getaway options from a user's departure city, including transport, hotel, attractions, and estimated total cost.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hello-ahang](https://clawhub.ai/user/hello-ahang)

### License/Terms of Use:

MIT-0

## Use Case:

Travelers and travel-planning agents use this skill to turn a short weekend travel request into three actionable package-style options with transportation, lodging, attractions, booking links, and budget estimates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow may install or upgrade a global FlyAI CLI package, including a documented sudo fallback.

Mitigation: Prefer a pinned, user-scoped install and do not run sudo package installation without explicit review and user consent.

Risk: The workflow documents disabling TLS certificate verification for FlyAI commands when SSL errors occur.

Mitigation: Do not set NODE_TLS_REJECT_UNAUTHORIZED=0; fix certificate, proxy, or network configuration instead.

Risk: The skill can read and save travel profile data such as home city, budget, companions, family details, and preferences.

Mitigation: Ask for explicit consent before reading or saving profile data, minimize stored details, and keep local profile files access-controlled.

Risk: Trip prices, ticket availability, hotel inventory, and attraction booking requirements can change after search results are returned.

Mitigation: Treat results as decision support and verify price, availability, cancellation terms, and reservation requirements before booking.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hello-ahang/skills/flyai-weekend-trip)
- [Workflow](artifact/reference/workflow.md)
- [User profile storage](artifact/reference/user-profile-storage.md)
- [Keyword search](artifact/reference/keyword-search.md)
- [Flight search](artifact/reference/search-flight.md)
- [Train search](artifact/reference/search-train.md)
- [Hotel search](artifact/reference/search-hotel.md)
- [POI search](artifact/reference/search-poi.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown travel plan with inline command guidance and booking links when available]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces three differentiated itinerary options with live-search-dependent prices and availability.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
