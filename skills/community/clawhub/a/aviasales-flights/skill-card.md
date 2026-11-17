## Description:

Searches for cheap flights and airfare via the Travelpayouts/Aviasales API, including date-specific fares, price calendars, round trips, latest prices, popular destinations, and IATA code lookup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aspalagin](https://clawhub.ai/user/aspalagin)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel assistants use this skill to look up fares, compare cheaper travel dates, resolve IATA codes, and present booking links from Aviasales/Travelpayouts search results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Flight search details and the Travelpayouts API token are used with external Travelpayouts/Aviasales services.

Mitigation: Install only when users accept that data flow, keep TRAVELPAYOUTS_TOKEN managed as a secret, and avoid submitting unnecessary personal travel data.

Risk: The airline mapping cache uses a shared temporary path at /tmp/airlines_cache.json.

Mitigation: Use a private per-user cache directory or run the skill in an isolated environment before deployment.

## Reference(s):

- [Airline code mapping](references/airlines.md)
- [ClawHub skill page](https://clawhub.ai/aspalagin/skills/aviasales-flights)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [JSON flight-search results that an agent can summarize as Markdown with prices, itinerary details, and booking links.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Most searches require TRAVELPAYOUTS_TOKEN; IATA lookup can run without the token.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
