## Description:

Guides agents through Scavio's Airbnb stay search, listing details, and guest reviews using structured API responses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scavio-ai](https://clawhub.ai/user/scavio-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Travel planners and short-term-rental researchers use this skill to compare stays, inspect listing amenities and ratings, and summarize guest feedback through Scavio.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms, listing IDs, travel dates, and guest counts are sent to Scavio, and API calls consume paid credits.

Mitigation: Disclose external data sharing and credit use before making requests; limit calls to what the task needs.

Risk: Review and host information may contain personal data.

Mitigation: Summarize information for travel or market research; do not profile individuals.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/scavio-ai/skills/airbnb-scraper-api)
- [Scavio Airbnb search documentation](https://scavio.dev/docs/airbnb-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=airbnb-scraper-api)
- [Scavio rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=airbnb-scraper-api)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands]

**Output Format:** [Markdown with API request examples and JSON response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Scavio API key; each API call consumes a credit.]

## Skill Version(s):

1.0.5 (source: server-resolved ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
