## Description: <br>
聚合并整理多源新闻，按科技/财经/AI/智能体分类排序，生成 Markdown 摘要并可定时执行。当用户提到"新闻"、"今日新闻"、"整理新闻"、"科技新闻"、"财经新闻"、"AI 新闻"、"智能体新闻"、"聚合新闻"或需要定时获取新闻摘要时使用。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[binbin1213](https://clawhub.ai/user/binbin1213) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to collect public news from configured sources, classify stories across technology, finance, AI, and agent categories, and produce daily Markdown news briefs. It also guides setup, scheduling, configuration changes, local file output, and optional channel delivery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches public news sources and may save generated summaries and logs under the user's home directory. <br>
Mitigation: Review configured sources, output paths, and generated Markdown before relying on or retaining the summaries. <br>
Risk: Optional scheduling and channel delivery can run automatically or send summaries to unintended recipients if configured incorrectly. <br>
Mitigation: Inspect cron entries, OpenClaw channel targets, and push settings before enabling scheduled or pushed briefs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/binbin1213/daily-news-brief-zh) <br>
- [Quick start guide](QuickStartGuide.md) <br>
- [Setup workflow](workflows/Setup.md) <br>
- [FetchNews workflow](workflows/FetchNews.md) <br>
- [Configure workflow](workflows/Configure.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown summaries, configuration JSON, and shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write dated Markdown news briefs and logs under the user's home directory and can optionally send summaries through configured OpenClaw channels.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
