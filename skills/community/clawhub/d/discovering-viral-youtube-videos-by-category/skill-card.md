## Description:

Discovers trending and viral YouTube videos by category and country using apidojo's YouTube Trending Scraper on Apify, returning titles, engagement metrics, channel details, duration, keywords, thumbnails, and ranking labels for content research.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apidojo-io](https://clawhub.ai/user/apidojo-io)

### License/Terms of Use:

MIT-0

## Use Case:

External content strategists, YouTubers, trend researchers, and developers use this skill to find and rank trending YouTube videos by category, country, and language for content planning and market research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses Apify and may require an APIFY_TOKEN for YouTube trend lookups.

Mitigation: Use a scoped token, keep it out of prompts, URLs, and saved result files, and rotate it if exposure is suspected.

Risk: Custom mapping functions or query parameters could expose secrets or private data to the external Apify actor.

Mitigation: Avoid including secrets or private data in customMapFunction, country, language, or other actor inputs.

Risk: YouTube trending data changes throughout the day and represents a snapshot.

Mitigation: Record the collection time, country, language, category, and maxItems with any report or downstream decision.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/apidojo-io/skills/discovering-viral-youtube-videos-by-category)
- [Apify YouTube Trending Scraper API endpoint](https://api.apify.com/v2/acts/apidojo~youtube-trending-scraper/runs)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, API Calls, Code, Configuration]

**Output Format:** [Markdown guidance with inline shell commands, REST API examples, scoring logic, and tabular video results guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save Apify actor results as CSV or JSON and ranks videos as MEGA_VIRAL, TRENDING, or RISING.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
