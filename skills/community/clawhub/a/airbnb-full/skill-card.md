## Description:

Complete Airbnb toolkit — search, availability, listing detail, price, cross-OTA price comparison and reviews, all in one unified schema.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stayingapi](https://clawhub.ai/user/stayingapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agents use this skill to retrieve Airbnb and related lodging data through StayingAPI, including search results, availability, listing details, prices, cross-OTA comparisons, and reviews.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Airbnb-related search details are sent to StayingAPI when the skill makes external API requests.

Mitigation: Install only when that data sharing is acceptable, and use sandbox credentials for evaluation before switching to live data.

Risk: The required StayingAPI key could be exposed through shell history, logs, or persistent profile files.

Mitigation: Store the key in an agent or OS secret store when possible, avoid logging it, and rotate or revoke it if exposure is suspected.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/stayingapi/skills/airbnb-full)
- [StayingAPI Homepage](https://stayingapi.com)
- [StayingAPI Documentation](https://stayingapi.com/docs)
- [StayingAPI OpenAPI Contract](https://api.stayingapi.com/openapi.json)
- [StayingAPI MCP Server](https://mcp.stayingapi.com/mcp)
- [StayingAPI Pricing](https://stayingapi.com/pricing)
- [StayingAPI Auth Setup](references/auth-setup.md)

## Skill Output:

**Output Type(s):** [API calls, JSON, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown guidance with REST or MCP calls and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires STAYINGAPI_KEY for API requests; sandbox keys return deterministic fixtures.]

## Skill Version(s):

1.1.0 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
