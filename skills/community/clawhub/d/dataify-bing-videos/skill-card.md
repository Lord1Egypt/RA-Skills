## Description:

Search Bing Videos for video results. Do not use for general Bing web search or media-file downloads.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dataify-server](https://clawhub.ai/user/dataify-server)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn a Bing Videos search request into Dataify Scraper API parameters and receive video search results. It supports filters such as market, language, duration, freshness, resolution, source site, and price when those constraints are requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API-token handling and setup guidance require review before installation.

Mitigation: Use a short-lived or least-privilege Dataify token, avoid passing it with --token, and prefer a session-scoped environment variable.

Risk: Search queries are sent to Dataify's service during live API calls.

Mitigation: Do not submit sensitive queries unless the user is comfortable sending them to Dataify.

## Reference(s):

- [Dataify Bing Videos API Reference](artifact/references/api.md)
- [ClawHub Skill Page](https://clawhub.ai/dataify-server/skills/dataify-bing-videos)
- [Dataify Publisher Profile](https://clawhub.ai/user/dataify-server)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, parameter tables, and API results as JSON or HTML when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses DATAIFY_API_TOKEN for live API calls; returns raw JSON or HTML only when explicitly requested.]

## Skill Version(s):

1.3.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
