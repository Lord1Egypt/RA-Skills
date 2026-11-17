## Description:

Compare public Agoda and Expedia flight offers through Crawlora using matched routes, dates, passenger counts, cabins, prices, and connection details.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crawlora-org](https://clawhub.ai/user/crawlora-org)

### License/Terms of Use:

MIT-0

## Use Case:

Travel planners and agents use this skill to shortlist public flight offers and explain itinerary tradeoffs, price basis, and missing fare conditions. Comparisons distinguish one-way offers from departing legs of round trips.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Flight search criteria and supplied request bodies are sent to Crawlora using an API key.

Mitigation: Send only necessary travel criteria, omit unrelated personal data, and protect the API key.

Risk: Observed prices and itineraries may not reflect final availability, fees, or completed round-trip coverage.

Mitigation: Label the search snapshot and price basis, flag missing fare conditions, and verify booking details before purchase.

## Reference(s):

- [Flight Itinerary Comparison on ClawHub](https://clawhub.ai/crawlora-org/skills/flight-itinerary-comparison)
- [Flight search endpoint reference](reference/endpoints.md)

## Skill Output:

**Output Type(s):** [Analysis, Guidance]

**Output Format:** [Markdown itinerary comparison and tradeoff brief]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes price basis, observed source details, and missing conditions; does not book flights.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
