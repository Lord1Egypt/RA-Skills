## Description: <br>
Query real-time Chinese commodity futures, financial index futures, crude oil, and shipping index prices across all exchanges. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhaocaixia888](https://clawhub.ai/user/zhaocaixia888) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, analysts, and developers use this skill to ask an agent for current Chinese futures quote snapshots and formatted comparisons across supported contracts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent may make web or curl requests to Sina Finance for requested futures contract symbols. <br>
Mitigation: Install only if that network access is acceptable, and review requested contract symbols before execution. <br>
Risk: Returned prices are market data for reference and may be delayed, unavailable, or unsuitable for trading decisions. <br>
Mitigation: Verify important trading decisions with an official exchange, broker, or other authoritative market data source. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhaocaixia888/china-commodity-quotes) <br>
- [Publisher profile](https://clawhub.ai/user/zhaocaixia888) <br>
- [Sina Finance](https://finance.sina.com.cn) <br>
- [Sina Finance futures quote page pattern](https://finance.sina.com.cn/futures/quotes/<CODE>.shtml) <br>
- [Sina Finance continuous contract quote API example](https://hq.sinajs.cn/list=IF0,IC0,IH0,IM0,SC0,EC0) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with quote summaries, compact tables, and optional inline curl commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require curl and may use SINARA_REFERER to set a custom Sina Finance referer header.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
