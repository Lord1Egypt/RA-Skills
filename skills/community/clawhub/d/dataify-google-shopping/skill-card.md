## Description:

Search Google Shopping for product discovery, offers, and price comparison.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dataify-server](https://clawhub.ai/user/dataify-server)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn Google Shopping requests into Dataify API calls for product discovery, offer lookup, and price comparison.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Shopping queries, filters, and optional location data are sent to Dataify.

Mitigation: Use the skill only when that data sharing is acceptable, and avoid including sensitive personal information in shopping queries.

Risk: The skill requires a Dataify API token and can accept it as a command argument.

Mitigation: Prefer DATAIFY_API_TOKEN, never paste the token into chat, and do not print or expose credential values.

Risk: Bulk scraping or multi-page collection can increase scope and cost.

Mitigation: Review parameters, cost, and scope before high-volume or multi-page use.

## Reference(s):

- [Dataify Google Shopping API Reference](artifact/references/google_shopping_api.md)
- [ClawHub Skill Page](https://clawhub.ai/dataify-server/skills/dataify-google-shopping)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and compact shopping results; raw JSON or HTML when explicitly requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call the Dataify Scraper API and return product titles, links, prices, offer details, counts, or raw response bodies depending on the requested output mode.]

## Skill Version(s):

1.3.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
