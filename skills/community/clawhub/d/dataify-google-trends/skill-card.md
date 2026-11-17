## Description:

Search Google Trends for keyword interest and trend data through the Dataify Scraper API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dataify-server](https://clawhub.ai/user/dataify-server)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to convert Google Trends requests into Dataify Scraper API calls and return the resulting trend data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends Google Trends query parameters to Dataify's external API.

Mitigation: Avoid sensitive search terms and use the skill only when external submission to Dataify is acceptable.

Risk: The skill requires a Dataify API token.

Mitigation: Configure DATAIFY_API_TOKEN through the environment, never paste it into chat, and avoid displaying token values in outputs.

## Reference(s):

- [Dataify Google Trends API Reference](references/google_trends_api.md)
- [Dataify Scraper API endpoint](https://scraperapi.dataify.com/request)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown or raw API response text, depending on the user's requested output mode]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include JSON, HTML, CSV-oriented results, or a pre-call parameter table; token values should not be displayed.]

## Skill Version(s):

1.3.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
