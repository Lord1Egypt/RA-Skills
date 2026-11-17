## Description:

Aggregates Chinese hot-trend lists from Zhihu, Weibo, Baidu, Bilibili, Douyin, and Toutiao, with optional JSON output and content-topic recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[freedompixels](https://clawhub.ai/user/freedompixels)

### License/Terms of Use:

MIT-0

## Use Case:

External users and content operators use this skill to fetch current Chinese-platform trend lists, compare cross-platform heat, and generate lightweight content-topic angles from public trend data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes live requests to public third-party trend endpoints, so results may be unavailable, rate-limited, or region-dependent.

Mitigation: Handle empty or partial platform results as expected operating conditions and rerun or narrow the platform selection when needed.

Risk: Short trend-related prompts may activate the skill even when the user did not intend to fetch Chinese platform trends.

Mitigation: Invoke it only when the user asks for hot trends, current hotspots, or platform trend rankings, and clarify the target platform if the request is ambiguous.

Risk: Trend data and generated topic angles can reflect fast-changing or platform-specific popularity signals rather than verified facts.

Mitigation: Treat output as discovery guidance and verify important claims against the linked source platform pages before publication or decision-making.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/freedompixels/skills/cn-hot-trends-6)
- [Zhihu hot-list API](https://api.zhihu.com/topstory/hot-lists/total?limit={})
- [Weibo hot-search API](https://weibo.com/ajax/side/hotSearch)
- [Baidu realtime board API](https://top.baidu.com/api/board?platform=wise&tab=realtime)
- [Bilibili ranking API](https://api.bilibili.com/x/web-interface/ranking/v2?rid=0&type=all)
- [Douyin web search endpoint](https://www.douyin.com/aweme/v1/web/general/search/single/?keyword_type=0&count={}&device_platform=webapp&aid=6383)
- [Toutiao hot-board feed endpoint](https://www.toutiao.com/api/pc/feed/?tab_name=hot_board&category=hot_board)

## Skill Output:

**Output Type(s):** [text, JSON, guidance, shell commands]

**Output Format:** [Terminal text report or JSON array, with optional Markdown-style topic recommendation text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports platform selection, per-platform result limits, JSON output, and optional content-topic recommendations.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
