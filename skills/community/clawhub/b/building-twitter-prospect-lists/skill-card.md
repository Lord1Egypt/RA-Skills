## Description:

Builds targeted B2B prospect lists from Twitter/X profiles and posts using apidojo's Twitter scrapers on Apify.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apidojo-io](https://clawhub.ai/user/apidojo-io)

### License/Terms of Use:

MIT-0

## Use Case:

Sales and growth teams use this skill to find Twitter/X users who match an ideal customer profile, enrich candidate profiles, filter by business criteria, and produce a prioritized prospect list for outreach.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow uses an Apify API token and includes query-string curl examples that can expose secrets through shell history, logs, or shared URLs.

Mitigation: Treat APIFY_TOKEN as a secret and prefer header-based authentication or protected MCP/secret configuration instead of query-string token usage.

Risk: Prospect lists can contain saved profile, bio, location, and recent activity data from Twitter/X users.

Mitigation: Store exported prospect lists in controlled locations and define retention and deletion practices before sharing or reusing the data.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/apidojo-io/skills/building-twitter-prospect-lists)
- [Apify Tweet Scraper Run Endpoint](https://api.apify.com/v2/acts/apidojo~tweet-scraper/runs?token=$APIFY_TOKEN)
- [Apify Twitter User Scraper Run Endpoint](https://api.apify.com/v2/acts/apidojo~twitter-user-scraper/runs?token=$APIFY_TOKEN)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, API Calls, Configuration]

**Output Format:** [Markdown with tables, ranked lists, and inline bash or tool-call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include CSV or JSON export guidance for saved prospect lists.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
