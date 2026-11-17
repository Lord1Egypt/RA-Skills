## Description:

Search 24+ airline loyalty programs for award space with miles cost, seat availability, and jetlag scores.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kurosh87](https://clawhub.ai/user/kurosh87)

### License/Terms of Use:


## Use Case:

External travelers and travel-planning agents use this skill to search airline award availability, compare mileage prices, review seat availability and jetlag scores, calculate cents-per-point value, and manage saved award trips or alerts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may use travel itinerary data, award-alert state, transfer-partner or payment-card context, external price lookup, and optional airline login sessions.

Mitigation: Use only accounts and profile data appropriate for award-search workflows, and confirm alert creation or logged-in airline actions before proceeding.

Risk: Award and cash-price checks rely on external services, cached data, rate limits, and sometimes protected airline booking pages.

Mitigation: Prefer the API cache for general searches, batch route queries within the documented limits, and use browser access only for visual verification or logged-in airline actions.

Risk: Airline frequent-flyer credentials may be required for booking-page searches behind login walls.

Mitigation: Require user-provided credentials only for the active session and do not store or log them.

## Reference(s):

- [Scrapling Documentation](https://scrapling.readthedocs.io/en/latest/overview.html)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration]

**Output Format:** [Markdown guidance with API request examples and structured travel-award result summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs can include award pricing in miles or points, seat availability, jetlag scores, fuel-surcharge warnings, transfer options, cents-per-point calculations, saved-trip summaries, and alert setup guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
