## Description:

Fetch and summarize the latest video game news from major gaming outlets, including IGN, Kotaku, GameSpot, Polygon, Eurogamer, Rock Paper Shotgun, VG247, Gematsu, and PlayStation Blog.

This skill is ready for commercial/non-commercial use.

## Publisher:

[byeolbit](https://clawhub.ai/user/byeolbit)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to get concise gaming-news briefings from major outlets, filtered by general interest, platform, region, business topic, or review coverage. It can also provide deeper summaries of specific stories when requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill fetches public gaming-news RSS feeds and may fetch article pages for deeper summaries.

Mitigation: Review fetched links and summaries before relying on them, and restrict network access to approved public news sources in controlled environments.

Risk: Installing with an unpinned ClawHub installer version can introduce unreviewed installer changes.

Mitigation: Use a pinned ClawHub installer version when stricter supply-chain controls are required.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/byeolbit/skills/gamer-news)
- [Gamer News Skill Repository](https://github.com/byeolbit/gamer-news-skill)
- [IGN RSS Feed](https://feeds.ign.com/ign/all)
- [Kotaku RSS Feed](https://kotaku.com/rss)
- [GameSpot RSS Feed](https://www.gamespot.com/feeds/mashup/)
- [Polygon RSS Feed](https://www.polygon.com/rss/index.xml)
- [Eurogamer RSS Feed](https://eurogamer.net/feed)
- [Rock Paper Shotgun RSS Feed](https://www.rockpapershotgun.com/feed)
- [VG247 RSS Feed](https://vg247.com/feed)
- [Gematsu RSS Feed](https://gematsu.com/feed)
- [PlayStation Blog RSS Feed](https://blog.playstation.com/feed)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown news briefing with story titles, source names, links, and short summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Matches the user's language and returns up to 5 stories by default, or up to 10 when requested.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
