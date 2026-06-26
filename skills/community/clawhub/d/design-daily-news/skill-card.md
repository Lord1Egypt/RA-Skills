## Description: <br>
每日设计与科技资讯聚合 - 从优设读报、36氪、虎嗅自动抓取并筛选最新的设计、AI、产品等行业动态。使用此技能获取最新的设计行业新闻、AI 趋势或每日新闻摘要。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tianyuvision-max](https://clawhub.ai/user/tianyuvision-max) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to generate a daily Chinese-language design and technology news digest from 优设读报, 36氪, and 虎嗅. It is suited for summarizing recent design, AI, product, and technology headlines into a concise Markdown report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs local Python and Bash scripts and makes outbound web requests to disclosed news sites. <br>
Mitigation: Review the scripts before installation and run only in an environment where these web requests are acceptable. <br>
Risk: The skill writes small cache, log, and archive files during normal operation. <br>
Mitigation: Confirm the configured local paths are appropriate and monitor cache or log retention if scheduled. <br>
Risk: The optional auto-fetch helper calls a local workspace script outside this package. <br>
Mitigation: Inspect and approve that external workspace script before adding the helper to cron or another scheduler. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tianyuvision-max/design-daily-news) <br>
- [优设读报](https://www.uisdc.com/news) <br>
- [36氪](https://36kr.com) <br>
- [36氪 RSS feed](https://36kr.com/feed) <br>
- [虎嗅](https://www.huxiu.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands] <br>
**Output Format:** [Markdown daily digest with linked headlines, source labels, summaries, and item counts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Daily report is capped at 15 items and may use local cache files for fetched source data.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
