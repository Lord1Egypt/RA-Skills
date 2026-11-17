## Description:

Aggregates trending topics from public hot lists such as Weibo, Zhihu, Douyin, Baidu, and tech/news feeds, then generates AI-friendly daily reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linzmin](https://clawhub.ai/user/linzmin)

### License/Terms of Use:

MIT-0

## Use Case:

External users, content analysts, and agent builders use this skill to collect public trending-topic feeds, deduplicate items, and prepare daily summaries that agents can reference in conversation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence reports unsafe shell execution in the message-sending path.

Mitigation: Use the skill only in a contained environment and do not run with --send or npm run daily until the sender is replaced with a non-shell API or execFile-style call.

Risk: The security evidence reports broad hard-coded local/OpenClaw paths that make installation risky.

Mitigation: Make data paths install-relative and validate them before enabling scheduled fetch or report jobs.

Risk: Generated reports summarize public feeds and may contain unverified or misleading items.

Mitigation: Treat generated reports as untrusted summaries and verify source links before using them in agent responses.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/linzmin/skills/ai-hotspot-daily)
- [Weibo Hot Search RSSHub Route](https://rsshub.app/weibo/search/hot)
- [Zhihu Hotlist RSSHub Route](https://rsshub.app/zhihu/hotlist)
- [Douyin Hotlist RSSHub Route](https://rsshub.app/douyin/hotlist)
- [Baidu Hotsearch RSSHub Route](https://rsshub.app/baidu/hotsearch)
- [36Kr Latest News RSSHub Route](https://rsshub.app/36kr/news/latest)
- [Huxiu RSS Feed](https://www.huxiu.com/rss/1.xml)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance]

**Output Format:** [Markdown and JSON daily hotspot reports with terminal status text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Fetches public feed items, deduplicates by simplified title, adds rule-based sentiment and conversation suggestions, and can send report sections when configured.]

## Skill Version(s):

1.0.0 (source: frontmatter, package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
