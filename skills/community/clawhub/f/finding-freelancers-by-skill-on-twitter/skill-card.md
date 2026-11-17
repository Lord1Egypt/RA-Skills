## Description:

Finds freelancers and independent contractors to recruit using apidojo's Twitter scrapers on Apify.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apidojo-io](https://clawhub.ai/user/apidojo-io)

### License/Terms of Use:

MIT-0

## Use Case:

Agencies, startup operators, project managers, and recruiters use this skill to find and prioritize freelance or independent talent on Twitter/X by skill area, availability signals, recent activity, and profile evidence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Apify tokens can be exposed if placed directly in request URLs or shared logs.

Mitigation: Use the MCP server or a secure API client, keep APIFY_TOKEN in environment or secret storage, and avoid pasting token-bearing URLs into shared channels.

Risk: Twitter/X search terms, handles, and profile data may include personal or recruiting-sensitive information.

Mitigation: Limit collection to data needed for the sourcing task, follow applicable privacy and platform policies, and review candidate data before outreach or storage.

Risk: Local helper scripts can affect data handling or credential exposure.

Mitigation: Verify any local helper script before running it and use a least-privilege Apify token.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/apidojo-io/skills/finding-freelancers-by-skill-on-twitter)
- [Apify actor: apidojo/twitter-user-scraper](https://apify.com/apidojo/twitter-user-scraper)
- [Apify actor: apidojo/tweet-scraper](https://apify.com/apidojo/tweet-scraper)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, API calls, Guidance]

**Output Format:** [Markdown candidate report with tables, shell commands, and optional CSV or JSON export instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes candidate handles, names, profile-derived skill signals, client or availability indicators, follower counts, activity status, and fit scores.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
