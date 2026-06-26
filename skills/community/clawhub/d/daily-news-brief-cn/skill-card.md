## Description: <br>
每日新闻简报，自动抓取热点新闻并 AI 提炼重点。支持财经/科技/国际新闻，定时推送。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zt6558609-cpu](https://clawhub.ai/user/zt6558609-cpu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate scheduled Chinese daily news briefs across finance, technology, and international categories, with configurable sources and delivery timing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scheduled delivery can repeatedly send generated briefs through configured messaging routes. <br>
Mitigation: Enable the OpenClaw cron job only after reviewing the configured schedule and channel destinations. <br>
Risk: News summaries are generated from public web content and fallback sources, so results can be incomplete, outdated, or inaccurate. <br>
Mitigation: Review important items against their source links before relying on the brief for decisions. <br>
Risk: The skill executes a local SearXNG skill when fetching live results. <br>
Mitigation: Install and run it only in an environment where the local SearXNG skill and its dependencies are trusted. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/zt6558609-cpu/daily-news-brief-cn) <br>
- [Publisher profile](https://clawhub.ai/user/zt6558609-cpu) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Configuration, Shell commands, Guidance] <br>
**Output Format:** [Markdown news brief with configuration JSON and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Briefs are saved under scripts/output and can be scheduled through OpenClaw cron.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
