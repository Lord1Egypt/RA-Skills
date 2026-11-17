## Description:

Query real-time Chinese commodity futures, financial index futures, crude oil, and shipping index prices across all exchanges.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaocaixia888](https://clawhub.ai/user/zhaocaixia888)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to look up Chinese futures contract prices, trading hours, contract code conventions, and quote fields from Sina Finance. It is suitable for market quote lookup and formatted reporting, not trading execution or financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat market quote output as trading advice.

Mitigation: Present results as quote lookup only and avoid recommending trades, positions, or execution decisions.

Risk: Direct quote requests depend on Sina Finance pages or APIs and may fail without the expected referer header.

Mitigation: Use the documented referer setting or browser snapshot fallback, and clearly report unavailable or stale quote data.

Risk: Output uses Chinese futures terminology that may be unclear to non-Chinese readers.

Mitigation: Ask the agent to localize labels or explain contract terminology when serving users who need non-Chinese output.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zhaocaixia888/skills/china-commodity-quotes)
- [Publisher Profile](https://clawhub.ai/user/zhaocaixia888)
- [Sina Finance](https://finance.sina.com.cn)
- [Sina Finance Futures Quote Example](https://finance.sina.com.cn/futures/quotes/IF2606.shtml)
- [Sina Finance Continuous Contract API Example](https://hq.sinajs.cn/list=IF0,IC0,IH0,IM0,SC0,EC0)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with quote summaries, compact tables, and optional inline curl commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Chinese futures terminology and may require localization when non-Chinese output is desired.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
