## Description:

Search Google Hotels for hotel discovery, prices, or availability. Do not use to scrape a known Booking.com hotel URL.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dataify-server](https://clawhub.ai/user/dataify-server)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to translate Google Hotels search requests into Dataify Scraper API calls and receive compact hotel discovery, pricing, and availability results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Hotel search details and the Dataify API token are sent to Dataify.

Mitigation: Use the skill only when that data sharing is acceptable for the user's task and environment.

Risk: API tokens can be exposed or persisted unnecessarily through command-line arguments or shell startup-file setup examples.

Mitigation: Prefer a session-scoped DATAIFY_API_TOKEN value or a secret manager, avoid passing tokens with --token, avoid persistent shell startup-file examples unless explicitly accepted, and rotate any token already stored that way.

## Reference(s):

- [Dataify Google Hotels API](references/google_hotels_api.md)
- [Dataify Scraper API endpoint](https://scraperapi.dataify.com/request)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and text, with JSON or HTML only when explicitly requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns compact user-facing hotel results by default and preserves source links when available.]

## Skill Version(s):

1.3.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
