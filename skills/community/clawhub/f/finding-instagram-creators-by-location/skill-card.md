## Description:

Finds Instagram content creators and influencers posting from a specific location using apidojo's Instagram location scraper on Apify, returning creator handles, location post counts, estimated followers, engagement, and recent content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apidojo-io](https://clawhub.ai/user/apidojo-io)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing teams, agencies, and agents supporting regional campaigns use this skill to discover and rank local Instagram creators for geo-targeted influencer outreach.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Apify token exposure when using the REST fallback with a token in the request URL.

Mitigation: Prefer the MCP or helper script path, keep APIFY_TOKEN in the environment or a protected .env file, and avoid embedding the token directly in URLs.

Risk: Instagram location scrape requests may send sensitive or private location targets to Apify.

Mitigation: Use narrowly scoped Apify credentials and provide only location targets that are appropriate for the campaign, policy, and compliance context.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/apidojo-io/skills/finding-instagram-creators-by-location)
- [Apify actor: apidojo/instagram-location-scraper](https://apify.com/apidojo/instagram-location-scraper)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown tables with optional inline shell commands and JSON actor input examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May also save Apify actor results as CSV or JSON when using the helper script.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
