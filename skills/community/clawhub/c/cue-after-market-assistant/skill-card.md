## Description:

面向 A 股市场层面的盘后复盘，汇总指数、资金、板块与涨跌驱动，并整理持仓影响和次日观察要点。

This skill is ready for commercial/non-commercial use.

## Publisher:

[panting09266-ai](https://clawhub.ai/user/panting09266-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to review A-share market and sector performance after market close, understand reported market drivers and capital flows, and prepare next-day observation points. It is scoped to market-level analysis and does not provide single-stock technical analysis.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: The security scan reports a suspicious, medium-confidence mismatch between the stated market-analysis purpose and several reported behaviors, including document conversion and service or account checks.

Mitigation: Review the requested actions and generated commands before use, and keep execution limited to the market-recap task.

Risk: The security guidance reports credential exposure risk.

Mitigation: Keep API keys in local configuration and do not disclose them in chat or generated reports.

Risk: The security guidance reports that a code runner can be downloaded or updated from unpinned sources and executed.

Mitigation: Inspect the runner and pin a reviewed version or commit before executing it.

Risk: The security guidance reports recurring scheduling behavior.

Mitigation: Review the schedule and command before enabling recurring runs, and monitor the resulting activity.

Risk: Scan coverage is partial because two local references could not be resolved, so referenced material was not established as safe.

Mitigation: Review referenced materials independently before relying on or executing them.

## Reference(s):

- [Cue research runner (GitHub)](https://github.com/sensedeal/cue-skills)
- [Cue research runner mirror (Gitee)](https://gitee.com/sensedeal/cue-skills)

## Skill Output:

**Output Type(s):** [Analysis, Text, Markdown, HTML]

**Output Format:** [Structured Chinese market-recap report in Markdown, with an optional standalone HTML dashboard]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Market and sector level; excludes single-stock technical analysis.]

## Skill Version(s):

1.0.17 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
