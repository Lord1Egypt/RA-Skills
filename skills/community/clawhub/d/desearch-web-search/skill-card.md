## Description:

Search the web and get real-time SERP-style results with titles, URLs, and snippets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[okradze](https://clawhub.ai/user/okradze)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to retrieve current web search results from Desearch for queries that need titles, links, and snippets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries are sent to Desearch for processing.

Mitigation: Use the skill only for queries that are appropriate to share with Desearch.

Risk: The skill authenticates requests with DESEARCH_API_KEY from the environment.

Mitigation: Review Desearch account billing and key permissions before use, and rotate or revoke the key if it is exposed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/okradze/skills/desearch-web-search)
- [Desearch homepage](https://desearch.ai)
- [Desearch Web API reference](https://desearch.ai/docs/api-reference/get-web)
- [Desearch Console](https://console.desearch.ai)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [JSON responses or command-line text containing web result titles, URLs, and snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires DESEARCH_API_KEY and returns up to 10 results per page with pagination via --start.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
