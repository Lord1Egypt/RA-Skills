## Description:

聚合并整理多源新闻，按科技/财经/AI/智能体分类排序，生成 Markdown 摘要并可定时执行。

This skill is ready for commercial/non-commercial use.

## Publisher:

[binbin1213](https://clawhub.ai/user/binbin1213)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, developers, and operators use this skill to collect daily technology, finance, AI, and agent-related news from configured sources, classify it, and generate a concise Markdown briefing. It supports manual runs, scheduled execution, local archive files, and optional channel delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Configured custom news URLs may fetch untrusted or unsuitable content.

Mitigation: Use trusted RSS or official public sources, review new URLs before adding them, and avoid arbitrary feeds.

Risk: Fetched summaries can be pushed to external messaging channels.

Mitigation: Enable OpenClaw channel delivery only for intended targets and review channel configuration before scheduled or manual push runs.

Risk: Scheduled execution can run repeatedly through cron or OpenClaw cron.

Mitigation: Review each cron entry, confirm the command path and frequency, and inspect logs after enabling automation.

Risk: Dependency installation is not pinned by the skill evidence.

Mitigation: Pin and review npm dependencies before installing or running the TypeScript tools.

Risk: Cleanup or uninstall examples can remove local news archives or configuration.

Mitigation: Verify target directories before running any removal command and keep backups when retaining historical briefs matters.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/binbin1213/skills/daily-news-brief-zh)
- [36Kr RSS feed](https://36kr.com/feed)
- [Huxiu RSS feed](https://www.huxiu.com/rss/0.xml)
- [Caixin technology RSS feed](https://www.caixin.com/rss/rss_newstech.xml)
- [Jiqizhixin RSS feed](https://www.jiqizhixin.com/rss)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Chinese-language Markdown briefings, local Markdown files, console summaries, configuration JSON, and setup or run commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Briefings group items by category, include source attribution, and may be saved under ~/daily-news-brief/每日新闻/ or sent through configured OpenClaw channels.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
