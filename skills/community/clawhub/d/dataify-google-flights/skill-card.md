## Description:

Search Google Flights for fares and itineraries using the Dataify Scraper API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dataify-server](https://clawhub.ai/user/dataify-server)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to search Google Flights fares and itineraries through Dataify. It converts flight criteria into documented API parameters and returns compact, user-facing results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles a paid Dataify API token.

Mitigation: Use a session-scoped DATAIFY_API_TOKEN or a secret manager, avoid command-line token arguments, and do not place the token in shell startup files.

Risk: Flight routes, dates, passenger counts, filters, and API credit usage are sent to Dataify during live searches.

Mitigation: Review the request details before high-volume, no-cache, or deep-search calls, and avoid sending sensitive travel details unless Dataify processing is acceptable.

## Reference(s):

- [Dataify Google Flights API Reference](references/google_flights_api.md)
- [ClawHub Skill Page](https://clawhub.ai/dataify-server/skills/dataify-google-flights)
- [Dataify Scraper API Endpoint](https://scraperapi.dataify.com/request)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration guidance]

**Output Format:** [Markdown text with optional JSON or HTML API response bodies and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May submit route, date, passenger, filter, and output-format parameters to Dataify; dry-run output can be a parameter table.]

## Skill Version(s):

1.3.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
