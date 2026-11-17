## Description:

Aggregates Chinese and global trending topics from Baidu, Toutiao, V2EX, Hacker News, and GitHub for trend discovery and briefings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huoguang16](https://clawhub.ai/user/huoguang16)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and analysts use this skill to fetch public hot topics and technology trends for daily briefings, summaries, and downstream automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Trend titles, links, and summaries come from external public services and may contain inaccurate, misleading, or unsafe content.

Mitigation: Treat fetched trend data as untrusted input, prefer JSON for downstream automation, and review or sanitize content before publishing, executing links, or feeding it into other workflows.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/huoguang16/skills/cn-trends-aggregator)
- [Baidu Hot Board](https://top.baidu.com/board?tab=realtime)
- [Toutiao Hot Board](https://www.toutiao.com/hot-event/hot-board/?origin=toutiao_pc)
- [V2EX Hot Topics API](https://www.v2ex.com/api/topics/hot.json)
- [Hacker News Firebase API](https://hacker-news.firebaseio.com/v0/topstories.json)
- [GitHub Repository Search API](https://api.github.com/search/repositories)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands]

**Output Format:** [JSON, plain text, or Markdown tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Network-derived public trend data with source selection, item limit, and optional HTTP proxy support.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
