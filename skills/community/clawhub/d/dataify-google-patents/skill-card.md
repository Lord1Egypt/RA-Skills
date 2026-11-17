## Description:

Search Google Patents for patent records; do not use for Google Scholar papers or general web results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dataify-server](https://clawhub.ai/user/dataify-server)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to convert Google Patents search requests into Dataify Scraper API calls and receive patent-search results with relevant titles, links, and patent fields.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends patent-search queries, filters, and a Dataify API token to Dataify.

Mitigation: Install only when this data sharing is acceptable, keep the token in DATAIFY_API_TOKEN or a command argument, and do not paste API tokens into chat.

Risk: Security evidence says the skill can enable Google Scholar results even though the stated scope is Google Patents.

Mitigation: Keep scholar=false for patent-only searches until the publisher aligns the documented scope and implementation.

## Reference(s):

- [Dataify Google Patents API Reference](references/google_patents_api.md)
- [Dataify skill page](https://clawhub.ai/dataify-server/skills/dataify-google-patents)
- [Dataify API endpoint](https://scraperapi.dataify.com/request)
- [Dataify dashboard login](https://dashboard.dataify.com/login?utm_source=skill)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, parameter tables, and API response text or JSON when requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a Dataify API token and sends patent-search queries and filters to Dataify.]

## Skill Version(s):

1.3.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
