## Description:

Gets a real Booking.com price quote for specified listing dates and compares the property against StayingAPI-resolved offers to identify the cheapest rate.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stayingapi](https://clawhub.ai/user/stayingapi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-shopping agents use this skill to quote a specific Booking.com listing for selected dates and occupancy, then check whether StayingAPI can resolve cheaper cross-OTA offers for the same property.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Travel dates, occupancy, listing details, and API credentials are sent to StayingAPI when live API calls are made.

Mitigation: Use the skill only when that data sharing is acceptable; evaluate with a sandbox key first and store live keys in trusted credential storage.

Risk: Sandbox responses are fixtures and may not match the requested property, dates, or occupancy.

Mitigation: Do not present sandbox results as live prices; switch to a live key before making user-facing booking comparisons.

Risk: Cross-OTA comparison coverage varies and may return a single aggregated-lowest offer rather than multiple platform offers.

Mitigation: Check the number of returned offers and describe single-offer responses as limited coverage rather than a broad multi-platform comparison.

## Reference(s):

- [StayingAPI homepage](https://stayingapi.com)
- [StayingAPI documentation](https://stayingapi.com/docs)
- [StayingAPI OpenAPI contract](https://api.stayingapi.com/openapi.json)
- [Authentication setup](references/auth-setup.md)
- [ClawHub skill page](https://clawhub.ai/stayingapi/skills/booking-com-prices)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with REST API request parameters and optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include API-call guidance and polling instructions; no files are produced by the skill.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
