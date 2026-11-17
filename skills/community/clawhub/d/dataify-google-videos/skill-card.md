## Description:

Searches Google Videos for video results through the Dataify Scraper API, excluding YouTube media downloads or structured YouTube records.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dataify-server](https://clawhub.ai/user/dataify-server)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to translate Google Videos search requests into Dataify Scraper API calls and receive concise video search results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credential handling can expose parts of a Dataify API token.

Mitigation: Configure the token through DATAIFY_API_TOKEN, avoid passing tokens on the command line or in chat, and avoid preview output with real credentials until the token masking issue is fixed.

## Reference(s):

- [Dataify Google Videos API](references/google_videos_api.md)
- [Dataify Scraper API request endpoint](https://scraperapi.dataify.com/request)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, JSON]

**Output Format:** [Markdown summaries, Markdown parameter tables, shell commands, and JSON or raw API responses when requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call the Dataify Scraper API and requires DATAIFY_API_TOKEN for live requests.]

## Skill Version(s):

1.3.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
