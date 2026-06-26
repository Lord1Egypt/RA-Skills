## Description: <br>
Fetches and summarizes the latest video game news from major gaming outlets including IGN, Kotaku, GameSpot, Polygon, Eurogamer, Rock Paper Shotgun, VG247, Gematsu, and PlayStation Blog. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byeolbit](https://clawhub.ai/user/byeolbit) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to request recent video game and gaming industry news, with source selection adapted to platform, region, business, review, or deeper-summary interests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts public gaming news RSS feeds and may load linked article pages when the user asks for deeper summaries. <br>
Mitigation: Install it only in environments where outbound access to those public sites is acceptable, and prefer the slash command or explicit news requests in restricted environments. <br>
Risk: News summaries can become stale or reflect inaccuracies in source articles. <br>
Mitigation: Keep summaries factual, include original links, and rely on the cited outlet pages for verification. <br>
Risk: Individual feeds can fail or return empty results. <br>
Mitigation: Skip failed feeds, use the next configured source, and note unavailable sources when showing partial results. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/byeolbit/gamer-news) <br>
- [Project homepage](https://github.com/byeolbit/gamer-news-skill) <br>
- [IGN RSS feed](https://feeds.ign.com/ign/all) <br>
- [Kotaku RSS feed](https://kotaku.com/rss) <br>
- [GameSpot RSS feed](https://www.gamespot.com/feeds/mashup/) <br>
- [Polygon RSS feed](https://www.polygon.com/rss/index.xml) <br>
- [Eurogamer RSS feed](https://eurogamer.net/feed) <br>
- [Rock Paper Shotgun RSS feed](https://www.rockpapershotgun.com/feed) <br>
- [VG247 RSS feed](https://vg247.com/feed) <br>
- [Gematsu RSS feed](https://gematsu.com/feed) <br>
- [PlayStation Blog RSS feed](https://blog.playstation.com/feed) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown news briefing with article links and concise summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Matches the user's language, shows up to 5 stories by default, and can summarize linked articles on request.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
