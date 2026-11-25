## Description:

帮助投资者复盘 A 股市场收盘表现，分析指数、资金流向、板块与涨跌驱动，并整理持仓影响和次日观察要点。

This skill is ready for commercial/non-commercial use.

## Publisher:

[panting09266-ai](https://clawhub.ai/user/panting09266-ai)

### License/Terms of Use:

MIT-0

## Use Case:

面向关注中国 A 股的投资者，用于收盘后了解市场、板块和资金表现，梳理市场层面的持仓影响，并准备次日观察要点；不用于单只个股分析。

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: The security review flags credential risk, and the artifact requests an API key for Cue access.

Mitigation: Do not share API keys in chat; configure credentials through a private, trusted method and review the skill before use.

Risk: The security review flags installation risk, and the artifact describes installing or updating a remote runner and executing it.

Mitigation: Review the remote code and its source before installing or updating it, and only run it if you trust the source and behavior.

Risk: The security guidance identifies recurring runs as an additional behavior to review.

Mitigation: Review what each scheduled run can access and do before enabling recurring execution.

## Reference(s):

- [Cue research runner (GitHub)](https://github.com/sensedeal/cue-skills)
- [Cue research runner (Gitee mirror)](https://gitee.com/sensedeal/cue-skills)
- [Eastmoney](https://www.eastmoney.com)
- [Tonghuashun](https://www.10jqka.com.cn)
- [Xueqiu](https://xueqiu.com)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, HTML]

**Output Format:** [Chinese market recap in structured Markdown, with a standalone HTML dashboard]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Market and sector level analysis; does not analyze individual stocks.]

## Skill Version(s):

1.0.18 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
