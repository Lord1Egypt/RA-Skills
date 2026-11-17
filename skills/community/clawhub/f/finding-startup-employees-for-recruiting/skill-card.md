## Description:

Finds professionals currently employed at startups to recruit using apidojo's Twitter scrapers on Apify.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apidojo-io](https://clawhub.ai/user/apidojo-io)

### License/Terms of Use:

MIT-0

## Use Case:

Technical recruiters, startup talent leads, and HR teams use this skill to find, enrich, score, and prioritize Twitter/X profiles of people currently employed at startups.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow collects identifiable recruiting targets and Twitter/X usernames through Apify.

Mitigation: Confirm compliance with platform terms, privacy requirements, and employment laws; set tight collection limits and minimize retention of candidate data.

Risk: The artifact includes token-bearing REST URL examples.

Mitigation: Use safer token handling such as authorization headers or environment-managed credentials, and avoid putting tokens in URLs, logs, or shared outputs.

Risk: Follower, following, or retweeter collection can expand candidate data collection beyond the recruiting task.

Mitigation: Avoid those collection modes unless necessary for the request and document the purpose and limits before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/apidojo-io/skills/finding-startup-employees-for-recruiting)
- [Apify twitter-user-scraper actor](https://apify.com/apidojo/twitter-user-scraper)
- [Apify tweet-scraper actor](https://apify.com/apidojo/tweet-scraper)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls, Guidance]

**Output Format:** [Markdown candidate tables with inline shell, MCP, and REST examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include candidate handles, profile attributes, scoring, activity labels, and bio excerpts.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
