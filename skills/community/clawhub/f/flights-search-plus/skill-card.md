## Description:

Searches live flight prices through the 51smart flight API for one-way, round-trip, and multi-date price calendar queries, including city-to-IATA conversion and structured result formatting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[syf8888](https://clawhub.ai/user/syf8888)

### License/Terms of Use:


## Use Case:

External users and travel-facing agents use this skill to collect trip details, run live flight searches, compare prices across dates, and present structured flight options.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live flight searches send route, date, passenger count, and cabin class details to the 51smart API.

Mitigation: Confirm the user wants a live flight search before making the API call, especially in vague travel conversations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/syf8888/skills/flights-search-plus)
- [51smart flight search API endpoint](https://skill.flight.51smart.com/api/search)

## Skill Output:

**Output Type(s):** [Text, Markdown, API calls, Guidance]

**Output Format:** [Markdown-style structured flight summaries and JSON HTTP POST request bodies]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include route, schedule, price, tax, baggage, seat-availability, and date-comparison details returned by the flight API.]

## Skill Version(s):

1.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
