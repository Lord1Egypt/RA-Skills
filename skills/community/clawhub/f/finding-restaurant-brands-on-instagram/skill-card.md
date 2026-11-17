## Description:

Discovers restaurant brands, food businesses, and hospitality accounts on Instagram using apidojo's Instagram Scraper on Apify.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apidojo-io](https://clawhub.ai/user/apidojo-io)

### License/Terms of Use:

MIT-0

## Use Case:

External sales, marketing, and business development teams use this skill to find and prioritize restaurant, food, and hospitality Instagram accounts for B2B outreach.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Instagram target URLs and resulting public account data are sent to Apify under the user's account or token.

Mitigation: Use approved target lists, review Apify and actor data handling for compliance needs, and avoid sensitive prospecting targets unless authorized.

Risk: Broad hashtags or unrestricted runs can collect noisy or excessive results.

Mitigation: Set explicit maxItems limits, use niche restaurant or food-business targets, filter consumer accounts, and deduplicate by username.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/apidojo-io/skills/finding-restaurant-brands-on-instagram)
- [Apify Instagram Scraper API endpoint](https://api.apify.com/v2/acts/apidojo~instagram-scraper/runs)
- [Example Instagram hashtag target](https://www.instagram.com/explore/tags/restaurantowner/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, REST API examples, scoring guidance, and optional CSV or JSON result files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Apify inputs such as startUrls, until, maxItems, and customMapFunction; recommends deduplicating accounts and filtering low-signal consumer profiles.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
