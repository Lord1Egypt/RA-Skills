## Description:

Retrieves 2026 Milan Winter Olympics medal standings, live news, China-specific medal results, and competition schedules from Baidu Sports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wuchubuzai2018](https://clawhub.ai/user/wuchubuzai2018)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to query Chinese-localized 2026 Milan Winter Olympics medal tables, live news, schedules, sport-specific schedules, and China team results through Baidu Sports data sources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends live network requests to Baidu Sports and returns Chinese-localized Olympics data that may have quality or transparency limitations.

Mitigation: Disclose Baidu Sports as the data source and verify important results against authoritative Olympics sources before relying on them.

Risk: Large or long-running scraping responses could strain memory-constrained agent environments.

Mitigation: Apply response-size limits and avoid unattended long-running use in constrained environments.

Risk: User-Agent rotation and locale behavior may be unclear to operators.

Mitigation: Review the scripts before deployment and document the request headers, User-Agent rotation, and Chinese locale assumptions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wuchubuzai2018/skills/baidu-milan-winter-olympics-2026)
- [Baidu Sports](https://tiyu.baidu.com/)
- [Baidu Sports 2026 Milan Winter Olympics medal page](https://tiyu.baidu.com/al/major/home?match=2026年米兰冬奥会&tab=奖牌榜)
- [Baidu Sports 2026 Milan Winter Olympics live news page](https://tiyu.baidu.com/al/major/home?match=2026年米兰冬奥会&tab=直击现场)
- [Baidu Sports 2026 Milan Winter Olympics schedule endpoint](https://tiyu.baidu.com/al/major/schedule/list)
- [Baidu Sports China delegation medal page](https://tiyu.baidu.com/al/major/delegation?id=26&match=2026年米兰冬奥会&tab=获奖名单)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and JSON data summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The underlying scripts return JSON-formatted Baidu Sports data for medal standings, news, schedules, sport lists, and China-specific results.]

## Skill Version(s):

0.0.2 (source: ClawHub release evidence, released 2026-02-10)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
