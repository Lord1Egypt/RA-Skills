## Description:

Fetches and analyzes current Douyin/TikTok trending topics, hashtags, songs, and creators using TikTok Creative Center as the primary data source.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lucasye378](https://clawhub.ai/user/lucasye378)

### License/Terms of Use:

MIT-0

## Use Case:

External users, marketers, creators, and analysts use this skill to ask an agent for current TikTok trend summaries, hashtag deep dives, regional popularity, audience insights, and content-trend analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Trend results may reflect TikTok Creative Center's English/global pages by default rather than a specific country, language, or China-specific Douyin market.

Mitigation: State the requested geography and language when summarizing results, and explicitly qualify global/default-source limits when no market-specific evidence is fetched.

Risk: Login-gated Creative Center pages can return empty or incomplete data.

Mitigation: Fall back to the public home page and hashtag pages, and tell the user when songs, videos, or creator details could not be retrieved.

Risk: Douyin-specific coverage is limited because China-specific Douyin data may block automated access.

Mitigation: Do not present TikTok Creative Center data as China-specific Douyin evidence unless the source fetched supports that claim.

Risk: Trend data changes frequently and can become stale quickly.

Mitigation: Record the fetch timestamp in the agent output and avoid reusing old trend summaries as current evidence.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lucasye378/skills/douyin-tiktok-trends)
- [TikTok Creative Center](https://ads.tiktok.com/business/creativecenter/)
- [TikTok Creative Center Trending Hashtags](https://ads.tiktok.com/business/creativecenter/inspiration/popular/hashtag/pc/en)
- [TikTok Creative Center Trends Home](https://ads.tiktok.com/business/creativecenter/trends/home/pc/en)
- [TikTok Creative Center Trending Creators](https://ads.tiktok.com/business/creativecenter/inspiration/popular/creator/pc/en)
- [TikTok Creative Center Videos Inspiration](https://ads.tiktok.com/business/creativecenter/inspiration/popular/pc/en)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown trend report with tables and optional simple Topic, Heat, and Trend lines]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires current web fetches; record the fetch timestamp; default source pages are global/English unless the user requests a qualified market.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
