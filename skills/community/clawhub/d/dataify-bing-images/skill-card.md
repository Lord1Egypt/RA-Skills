## Description:

Search Bing Images for image results. Do not use for Bing web, news, shopping, map, or video results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dataify-server](https://clawhub.ai/user/dataify-server)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to search Bing Images through Dataify and receive a compact list or gallery of relevant image results with titles, image URLs, dimensions, and source links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API tokens may be exposed through command-line arguments, chat messages, or persistent shell startup files.

Mitigation: Prefer DATAIFY_API_TOKEN scoped to the current session or stored through a credential manager; avoid the --token option and never paste real tokens into chat.

Risk: Image licensing may be unverified in ordinary search results.

Mitigation: Use the supported license filter when licensing matters and treat returned licensing details as needing review before commercial use.

Risk: The skill calls an external Dataify API endpoint and may consume account credits.

Mitigation: Confirm high-volume, multi-page, or cost-sensitive searches before execution and handle missing, invalid, or insufficient-credit account states without exposing credentials.

## Reference(s):

- [Dataify Bing Images API Reference](references/api.md)
- [ClawHub Skill Page](https://clawhub.ai/dataify-server/skills/dataify-bing-images)
- [Dataify Scraper API Endpoint](https://scraperapi.dataify.com/request)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown result summaries, with raw JSON or HTML only when explicitly requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results may include image title, image URL, dimensions, source link, count or truncation notes, and an unverified licensing note unless a license filter is requested.]

## Skill Version(s):

1.3.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
