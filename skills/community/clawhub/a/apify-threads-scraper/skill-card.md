## Description:

Helps an agent collect Meta Threads posts, search by keyword or hashtag, and retrieve engagement metrics through the Apify Threads scraper actor.

This skill is ready for commercial/non-commercial use.

## Publisher:

[futurizerush](https://clawhub.ai/user/futurizerush)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and external users use this skill to guide agents in starting Apify Threads scraper runs, polling for completion, and fetching JSON results for authorized Threads usernames, hashtags, or keyword searches.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Token-in-URL examples can expose APIFY_API_TOKEN values through logs, shell history, copied commands, or shared request URLs.

Mitigation: Prefer Authorization headers where supported, use a dedicated least-privilege Apify token, avoid logging full request URLs, and rotate any token that was used in copied commands or shared logs.

Risk: Threads usernames, keywords, run metadata, and scraped results are processed through Apify and the named third-party actor.

Mitigation: Use the skill only for Threads data the user is authorized to collect and process, disclose third-party handling where appropriate, and apply data minimization and retention controls.

## Reference(s):

- [Apify Threads Scraper Actor](https://apify.com/futurizerush/meta-threads-scraper?fpr=rush)
- [Apify API v2 Documentation](https://docs.apify.com/api/v2)
- [ClawHub Skill Page](https://clawhub.ai/futurizerush/skills/apify-threads-scraper)

## Skill Output:

**Output Type(s):** [guidance, code, shell commands, configuration]

**Output Format:** [Markdown guidance with Python and bash examples for Apify API calls and JSON results.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an APIFY_API_TOKEN and authorized Threads data collection scope.]

## Skill Version(s):

0.2.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
