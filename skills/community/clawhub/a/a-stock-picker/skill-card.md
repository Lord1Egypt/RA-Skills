## Description:

A股三层选股模型用于按量化筛选、定性分析和择时操作生成A股候选标的与操作方案。

This skill is ready for commercial/non-commercial use.

## Publisher:

[danpian1](https://clawhub.ai/user/danpian1)

### License/Terms of Use:

MIT-0

## Use Case:

External users and analysts use this skill to screen A-share equities, review candidate fundamentals and catalysts, and draft markdown stock-selection summaries with risk controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can produce precise trading recommendations even when documented safeguards are not fully enforced.

Mitigation: Treat outputs as screening leads only; require independent financial review, source-data checks, and explicit confirmation of stop-loss and position-sizing assumptions before action.

Risk: Incomplete market scans or unavailable data can be presented as actionable candidate lists.

Mitigation: Review scan coverage, skipped symbols, data freshness, and failed data calls before using any shortlist.

## Reference(s):

- [A股三层选股模型 ClawHub page](https://clawhub.ai/danpian1/skills/a-stock-picker)
- [量化筛选规则](references/screening-rules.md)
- [定性分析框架](references/analysis-framework.md)
- [新浪财经行情接口](https://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php)
- [腾讯行情K线接口](https://web.ifzq.gtimg.cn/appstock/app/fqkline/get)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown tables and concise Chinese analysis, with optional terminal output from the screening script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include initial screening results, qualitative scores, buy ranges, stop-loss levels, targets, position sizing, and risk labels.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
