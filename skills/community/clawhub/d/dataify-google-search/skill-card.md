## Description:

Run a general Google web or SERP search and return structured SERP results through Dataify.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dataify-server](https://clawhub.ai/user/dataify-server)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to run Google web or SERP searches, map search parameters to the Dataify Scraper API, and receive compact search results or raw JSON/HTML when requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries are sent to Dataify and may contain sensitive information.

Mitigation: Use the skill only for queries appropriate to share with Dataify, and avoid confidential or personal data in search terms.

Risk: The Dataify API token can be exposed or made persistent through command-line arguments or shell startup configuration.

Mitigation: Prefer a session-scoped environment variable or credential manager, avoid passing tokens with --token, and review any persistent shell changes before applying them.

## Reference(s):

- [Dataify Google Search API Reference](references/google_search_api.md)
- [Dataify Scraper API endpoint](https://scraperapi.dataify.com/request)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, API calls]

**Output Format:** [Markdown summaries with optional raw JSON or HTML.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a Dataify API token and sends form-encoded Google Search parameters to Dataify.]

## Skill Version(s):

1.3.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
