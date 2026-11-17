## Description:

Search Google Local for nearby businesses and local pack keyword-and-location results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dataify-server](https://clawhub.ai/user/dataify-server)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to run Google Local keyword-and-location searches through Dataify and receive compact local business results. Raw JSON or HTML can be requested when the user needs the original response format.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API tokens may be exposed if passed in chat, command arguments, logs, or previews.

Mitigation: Use DATAIFY_API_TOKEN from the shell environment or a secret manager, and avoid the --token argument for normal use.

Risk: Search queries and location fields are sent to Dataify.

Mitigation: Avoid submitting sensitive data in search terms or locations unless that disclosure is approved for the workflow.

Risk: The package accepts direct CID or Place ID lookup even though the advertised skill boundary excludes known Place ID and detailed map record use.

Mitigation: Use the skill for keyword-and-location Google Local searches, and treat direct CID or Place ID lookup as out of scope until the package aligns its documentation and code.

## Reference(s):

- [Dataify Google Local API](references/google_local_api.md)
- [Dataify Scraper API endpoint](https://scraperapi.dataify.com/request)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration guidance]

**Output Format:** [Compact Markdown summaries by default, with optional raw JSON, HTML, or parameter preview tables.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Dataify API token; search query, location, and related Google Local parameters are sent to Dataify.]

## Skill Version(s):

1.3.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
