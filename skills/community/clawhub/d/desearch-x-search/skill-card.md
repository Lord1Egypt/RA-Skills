## Description:

Search X (Twitter) in real time. Find posts by keyword, user, or hashtag. Get a user's timeline, replies, retweeters, or fetch specific posts by ID or URL. Supports advanced filters like date range, language, engagement thresholds, and media type.

This skill is ready for commercial/non-commercial use.

## Publisher:

[okradze](https://clawhub.ai/user/okradze)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to search and monitor X/Twitter content through Desearch, including post search, user timelines, replies, retweeters, and post lookup by ID or URL.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms, usernames, post URLs, IDs, filters, and API-key-authenticated requests are sent to Desearch.

Mitigation: Use the skill only when Desearch's handling policies meet the user's confidentiality, secrets, and regulated-data requirements.

Risk: Use requires a Desearch API key.

Mitigation: Provide the key through DESEARCH_API_KEY and avoid exposing it in prompts, logs, or shared command output.

## Reference(s):

- [Desearch Homepage](https://desearch.ai)
- [Desearch API Reference](https://desearch.ai/docs/api-reference)
- [Desearch Console](https://console.desearch.ai)
- [ClawHub Skill Page](https://clawhub.ai/okradze/skills/desearch-x-search)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration guidance, API calls]

**Output Format:** [Markdown with inline shell commands and JSON or text API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires DESEARCH_API_KEY and sends requests to Desearch's external API.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
