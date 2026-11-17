## Description:

Search Google Maps to discover places, businesses, or map results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dataify-server](https://clawhub.ai/user/dataify-server)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to convert Google Maps search requests into Dataify Scraper API calls and receive concise place or map-search results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary says the advertised Google Maps search scope conflicts with Place ID/CID and place-detail capabilities.

Mitigation: Use this skill for search, coordinates, zoom, and pagination workflows; avoid Place ID/CID detail workflows unless the publisher clarifies the intended scope.

Risk: Google Maps searches, coordinates, and place identifiers may be sent to Dataify with an API token.

Mitigation: Avoid sensitive queries and configure the token through DATAIFY_API_TOKEN rather than pasting credentials into chat.

## Reference(s):

- [Dataify Google Maps API Reference](references/google_maps_api.md)
- [Dataify Scraper API Request Endpoint](https://scraperapi.dataify.com/request)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with optional shell commands and raw JSON or HTML API responses when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require DATAIFY_API_TOKEN; API requests can include Google Maps search terms, coordinates, and place identifiers.]

## Skill Version(s):

1.3.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
