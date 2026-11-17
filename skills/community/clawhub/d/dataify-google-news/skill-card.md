## Description:

Search Google News for current news results. Do not use for general Google web search.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dataify-server](https://clawhub.ai/user/dataify-server)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to run Google News searches through the Dataify Scraper API and receive current news results or raw JSON/HTML when requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a Dataify API token and sends requests to Dataify.

Mitigation: Use a session-scoped DATAIFY_API_TOKEN, do not pass tokens on the command line, and verify only whether the variable is configured.

Risk: Persistent shell-profile setup can store the API token in plaintext.

Mitigation: Prefer session-only environment setup and avoid persistent profile edits unless the user understands the plaintext secret exposure.

Risk: The package includes broader non-news Dataify workflow scripts beyond the advertised Google News purpose.

Mitigation: Use only the Google News workflow for this release unless the extra scripts are separately reviewed and intentionally enabled.

## Reference(s):

- [Dataify Google News API Reference](references/google_news_api.md)
- [Dataify Google News ClawHub release](https://clawhub.ai/dataify-server/skills/dataify-google-news)
- [Dataify Scraper API request endpoint](https://scraperapi.dataify.com/request)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown summaries with source links by default; raw JSON or HTML only when requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires DATAIFY_API_TOKEN for live API calls; dry-run mode prints normalized form parameters without calling the API.]

## Skill Version(s):

1.3.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
