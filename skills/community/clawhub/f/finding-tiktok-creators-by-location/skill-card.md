## Description:

Discovers TikTok creators and content by geographic location using apidojo's TikTok Location Scraper on Apify.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apidojo-io](https://clawhub.ai/user/apidojo-io)

### License/Terms of Use:

MIT-0

## Use Case:

External marketers, researchers, and agents use this skill to find TikTok creators tied to a specific place and rank them for local outreach, geo-targeted influencer campaigns, or regional market research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: APIFY_TOKEN exposure could allow unauthorized Apify use.

Mitigation: Keep APIFY_TOKEN in environment or secret storage and do not paste it into shared prompts, files, or logs.

Risk: Location-based creator exports may contain personal or sensitive data.

Mitigation: Avoid sensitive inputs and store exported CSV/JSON only in approved locations for privacy and compliance needs.

Risk: TikTok location results may include irrelevant, duplicate, or stale creators.

Mitigation: Deduplicate by creator username and cross-check bios, recency, and location signals before campaign or outreach decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/apidojo-io/skills/finding-tiktok-creators-by-location)
- [Apify actor API endpoint](https://api.apify.com/v2/acts/apidojo~tiktok-location-scraper/runs)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples, API request examples, and ranking criteria]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save Apify actor results as CSV or JSON when requested; outputs can include creator usernames, follower counts, verification status, hashtags, video data, and engagement metrics.]

## Skill Version(s):

1.0.0 (source: server release evidence; artifact frontmatter metadata version 1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
