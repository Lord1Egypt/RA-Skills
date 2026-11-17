## Description:

基于可审计 A 股数据执行首板隔夜模拟策略的决策技能。用于评估当日首板赚钱效应、筛选首板候选、生成带证据的 BUY、WATCH 或 NO_TRADE 决策并制定 T+1 退出计划。当用户需要评估首板赚钱效应、做首板留仓决策、制定隔夜打板策略或复盘首板案例时触发（包含触发词：首板隔夜, 首板候选, 今晚要不要留首板, 隔夜打板, 涨停首板, first board overnight）。

This skill is ready for commercial/non-commercial use.

## Publisher:

[fize](https://clawhub.ai/user/fize)

### License/Terms of Use:

MIT-0

## Use Case:

External users and analysts use this skill to evaluate Chinese A-share first-board overnight simulated trading decisions, including candidate review, entry decisions, T+1 exit planning, and trade review. The skill is intended to produce auditable strategy reasoning rather than real-money trading execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may mistake simulated strategy output for real-money trading advice.

Mitigation: Use the skill for simulated strategy workflows only, and do not use it for real-money trading execution.

Risk: Missing, stale, or unrecoverable market data can make an entry decision unsupported.

Mitigation: Require auditable evidence, explicit unknowns, and READY, RESEARCH_ONLY, or BLOCKED status before acting on a decision.

Risk: Historical or closing data could be misused to imply unavailable intraday facts or executable fills.

Mitigation: Downgrade to RESEARCH_ONLY or BLOCKED when decision-time evidence is incomplete, and never represent historical research as a completed trade.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/fize/skills/first-board-overnight)
- [Strategy Definition](artifact/references/strategy.md)
- [Data Acquisition](artifact/references/data-acquisition.md)
- [Evidence Contract](artifact/references/evidence-contract.md)
- [Entry Policy](artifact/references/entry-policy.md)
- [Exit Policy](artifact/references/exit-policy.md)
- [Risk Policy](artifact/references/risk-policy.md)
- [Trade Review Schema](artifact/references/review-schema.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, code, configuration, guidance]

**Output Format:** [Markdown reports with structured decision fields, plus optional shell commands and SVG chart files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Saves standardized strategy reports under ./report/strategy when decisions are completed; may generate chart SVGs when requested.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
