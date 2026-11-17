## Description:

Generate daily geopolitical TikTok scripts using free news sources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ahmed181283](https://clawhub.ai/user/ahmed181283)

### License/Terms of Use:

MIT-0

## Use Case:

External content creators and social media teams use this skill to gather recent geopolitical RSS items and draft short-form TikTok scripts, daily report scripts, hashtags, and posting guidance. Developers may also use it as a configurable local workflow for regional or topic-specific geopolitical content generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: System-wide dependency installation can affect the host Python environment.

Mitigation: Install dependencies in a virtual environment or isolated tool environment before running the generator.

Risk: Cron, systemd, or Heartbeat scheduling can cause recurring automated news gathering and script generation.

Mitigation: Enable scheduling only when intentional and review the configured cadence, workspace path, and output location.

Risk: Generated geopolitical scripts may be incomplete, misleading, or overstate certainty because they rely on RSS summaries and attention-grabbing wording.

Mitigation: Review every generated script against the cited source article before recording or posting.

Risk: One configured feed uses HTTP rather than HTTPS.

Mitigation: Treat content from the HTTP feed with caution and prefer HTTPS feed sources where available.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ahmed181283/skills/daily-geo-tiktok)
- [BBC World RSS feed](http://feeds.bbci.co.uk/news/world/rss.xml)
- [Reuters World RSS feed](https://www.reuters.com/rssFeed/worldNews)
- [Reuters Conflict RSS feed](https://www.reuters.com/rssFeed/conflict)
- [AP World News RSS feed](https://storage.googleapis.com/afs-prod/media/feeds/AP.WorldNews.xml)
- [Al Jazeera RSS feed](https://www.aljazeera.com/xml/rss/all.xml)

## Skill Output:

**Output Type(s):** [text, markdown, json, configuration, guidance]

**Output Format:** [Plain text scripts, daily report text, metadata JSON, and Markdown usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated outputs are saved to timestamped local directories and may be filtered by time window, region, topic, and number of scripts.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
