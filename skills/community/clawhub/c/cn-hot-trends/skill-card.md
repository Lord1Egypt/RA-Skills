## Description:

Aggregates real-time hot lists from major Chinese platforms and summarizes trending search, discussion, technology, finance, entertainment, and music topics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sungang-pine](https://clawhub.ai/user/sungang-pine)

### License/Terms of Use:

MIT-0

## Use Case:

External users and analysts use this skill to ask for current Chinese-platform trending topics, either as a general multi-platform brief or filtered by platform or category.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may fetch data from multiple public Chinese websites for a trend request.

Mitigation: Use it only where outbound access to those public sites is acceptable, and limit requests to the platforms needed for the task.

Risk: Some platforms may return more complete results when cookies are supplied, which can share account-context data.

Mitigation: Do not provide platform cookies unless the user explicitly chooses to share them for a specific query.

Risk: Trending lists are time-sensitive and source pages can fail or change format.

Mitigation: Treat the output as a current brief from available sources and skip failed platforms rather than relying on a single list.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/sungang-pine/skills/cn-hot-trends)
- [Weibo Hot Search API](https://weibo.com/ajax/side/hotSearch)
- [Baidu Realtime Hot List](https://top.baidu.com/board?tab=realtime)
- [Zhihu Billboard](https://www.zhihu.com/billboard)
- [Douyin Hot List](https://www.douyin.com/hot)
- [Bilibili Popular Ranking](https://www.bilibili.com/v/popular/rank/all)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown trend brief with ranked lists, keyword summary, and optional PowerShell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Summaries are time-sensitive and depend on availability of the source platforms.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
