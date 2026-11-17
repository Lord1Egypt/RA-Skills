## Description:

Extracts and analyzes tweet history from competitor or brand Twitter profiles using apidojo's Twitter Profile Scraper on Apify, returning tweet text, engagement metrics, and author data for competitive intelligence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apidojo-io](https://clawhub.ai/user/apidojo-io)

### License/Terms of Use:

MIT-0

## Use Case:

External competitive intelligence, PR, and brand strategy teams use this skill to collect Twitter/X profile timelines, filter them by profile, date, media, or reply options, and rank posts by engagement for content strategy analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Twitter/X handles, profile URLs, date filters, and custom mapping content are sent to Apify when the actor is run.

Mitigation: Review inputs before execution, avoid including secrets or unnecessary sensitive data, and use an APIFY_TOKEN only in the intended execution environment.

Risk: Large actor runs may create cost or terms-of-use exposure for Twitter/X scraping through Apify.

Mitigation: Review Apify actor pricing and applicable terms before large runs, and constrain maxItems or date ranges when a smaller sample is sufficient.

## Reference(s):

- [Server-resolved GitHub provenance](https://github.com/apidojo-io/apidojo-skills/tree/main/skills/intent/analyzing-competitor-twitter-profile-content)
- [Apify Twitter Profile Scraper run API](https://api.apify.com/v2/acts/apidojo~twitter-profile-scraper/runs)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON actor inputs, scoring logic, and result handling notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can guide CSV or JSON result export from Apify actor runs and ranking of tweet records by engagement, views, and media presence.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact metadata version 1.0 differs)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
