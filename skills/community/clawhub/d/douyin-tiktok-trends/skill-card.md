## Description: <br>
Fetches current trending topics, hashtags, songs, and creators on Douyin/TikTok using TikTok Creative Center as the primary data source. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lucasye378](https://clawhub.ai/user/lucasye378) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketing, content strategy, and social media teams use this skill to fetch and summarize current TikTok/Douyin trends, including hashtags, songs, creators, and hashtag detail pages. Agents can use it when a user asks what is trending on TikTok or wants a concise trend analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may activate on broad trend or hot-topic requests that are not specifically about TikTok or Douyin. <br>
Mitigation: For ambiguous trend requests, confirm the intended platform before relying on this skill's output. <br>
Risk: Some Creative Center pages may be login-gated or return incomplete data. <br>
Mitigation: Fall back to public home and hashtag pages and clearly state when creator, song, or video details are unavailable. <br>
Risk: TikTok and Douyin trend data changes frequently and may become stale quickly. <br>
Mitigation: Include the fetch timestamp and avoid presenting trend rankings as durable facts. <br>
Risk: China-specific Douyin coverage is limited because automated access to Douyin data is restricted. <br>
Mitigation: Describe Douyin-specific results as limited coverage unless the fetched source directly supports the claim. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/lucasye378/douyin-tiktok-trends) <br>
- [TikTok Creative Center](https://ads.tiktok.com/business/creativecenter/) <br>
- [TikTok Creative Center Trending Hashtags](https://ads.tiktok.com/business/creativecenter/inspiration/popular/hashtag/pc/en) <br>
- [TikTok Creative Center Trends Home](https://ads.tiktok.com/business/creativecenter/trends/home/pc/en) <br>
- [TikTok Creative Center Trending Creators](https://ads.tiktok.com/business/creativecenter/inspiration/popular/creator/pc/en) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown trend summaries with tables, bullets, and optional simple Topic / Heat / Trend lines] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include fetch timestamps, ranked hashtags, songs, creators, post counts, commercial-use indicators, regional popularity, audience notes, and related interests.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
