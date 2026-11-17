## Description:

Researches video games across Steam and PlayStation Store using Crawlora's game data API, returning pricing, reviews, player counts, charts, and deals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crawlora-org](https://clawhub.ai/user/crawlora-org)

### License/Terms of Use:

MIT-0

## Use Case:

Players and game researchers use this skill to compare store listings, prices, reviews, popularity, and deals across Steam and PlayStation Store; the available public-data lookups also include Roblox experiences.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Game lookup queries and the Crawlora API key are sent to Crawlora.

Mitigation: Use a dedicated API key, keep it in CRAWLORA_API_KEY, and avoid sensitive information in lookup queries.

Risk: The helper includes public Roblox lookups that are not highlighted in the main Steam and PlayStation description.

Mitigation: Review the endpoint reference and allow Roblox lookups only if that broader scope is acceptable.

## Reference(s):

- [Crawlora game endpoint reference](reference/endpoints.md)
- [Crawlora](https://crawlora.net)
- [Gaming Research on ClawHub](https://clawhub.ai/crawlora-org/skills/gaming-research)

## Skill Output:

**Output Type(s):** [Text, Analysis, Guidance]

**Output Format:** [JSON game data and concise text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Public game data; pricing and availability can vary by storefront region.]

## Skill Version(s):

1.0.19 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
