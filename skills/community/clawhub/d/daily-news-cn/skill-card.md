## Description:

每日新闻自动采集与报告生成。双引擎交叉验证 + 官方媒体优先 + 900秒超时容错。v2.3 稳定运行版（2026-06-01）。

This skill is ready for commercial/non-commercial use.

## Publisher:

[paudyyin](https://clawhub.ai/user/paudyyin)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate Chinese daily news reports across politics, finance, AI, technology, consumer electronics, and home appliances. The skill searches current web sources, cross-checks numeric claims, returns a full Markdown report, and saves a local archive copy.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill performs multiple web searches and may include inaccurate, stale, or unverified source material in a daily report.

Mitigation: Review the generated report before relying on it, especially items marked as single-source or lower-confidence.

Risk: The skill can save persistent local archives of daily reports.

Mitigation: Delete memory/daily_news_*.md files or disable archiving if historical report retention is not desired.

Risk: The bundled cron example can trigger recurring automated news collection.

Mitigation: Review or disable the cron schedule before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/paudyyin/skills/daily-news-cn)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown report with source and confidence annotations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Also saves an archive copy under memory/daily_news_YYYY-MM-DD.md when executed.]

## Skill Version(s):

2.3.0 (source: frontmatter, package.json, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
