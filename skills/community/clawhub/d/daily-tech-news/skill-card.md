## Description: <br>
每日科技资讯聚合。自动抓取GitHub Trending、51CTO、百度热搜科技榜，筛选AI/Cloud/ML领域内容，生成结构化简报。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lgugeng](https://clawhub.ai/user/lgugeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Operators, editors, and automation users can use this skill to gather public technology news sources, deduplicate items, generate concise daily Markdown briefings, and optionally post reports to Feishu. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run on a schedule and post generated content to Feishu. <br>
Mitigation: Keep cron disabled until intentionally enabled, configure only trusted Feishu webhooks, and review generated reports before enabling automated posting. <br>
Risk: Filename handling for dates and briefing themes can write outside intended folders when given untrusted input. <br>
Mitigation: Validate TODAY and theme values against a strict allowlist before running the report generators. <br>
Risk: The configuration includes a hard-coded Feishu user_id. <br>
Mitigation: Remove or replace the user_id during deployment and keep workspace-specific recipients in local configuration. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lgugeng/daily-tech-news) <br>
- [Publisher profile](https://clawhub.ai/user/lgugeng) <br>
- [GitHub Trending](https://github.com/trending) <br>
- [Baidu Tech Hot List](https://top.baidu.com/board?tab=realtime&category=tech) <br>
- [Feishu webhook configuration](artifact/USAGE.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown briefings, JSON report files, Feishu message payloads, and setup commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes dated local report files under data/daily and briefings; Feishu delivery requires a configured webhook.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
