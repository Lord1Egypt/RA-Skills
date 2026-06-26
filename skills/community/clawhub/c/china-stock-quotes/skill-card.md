## Description: <br>
Query real-time A-share stock prices, major indices, and sector data across Shanghai, Shenzhen, and Beijing exchanges. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhaocaixia888](https://clawhub.ai/user/zhaocaixia888) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to retrieve and format A-share quotes, index snapshots, and sector-related market data for Shanghai, Shenzhen, and Beijing exchanges. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Security evidence flags helper behavior with broad execution permissions. <br>
Mitigation: Install only after reviewing the publisher and helper behavior; disable full-access review defaults when applicable and inspect diffs for secrets before use. <br>
Risk: Market data can be stale outside A-share trading hours or when the upstream quote service is unavailable. <br>
Mitigation: Check the quote timestamp, trading session, and upstream response before relying on the output for time-sensitive decisions. <br>


## Reference(s): <br>
- [China Stock Quotes on ClawHub](https://clawhub.ai/zhaocaixia888/china-stock-quotes) <br>
- [Sina Finance real-time quote page example](https://finance.sina.com.cn/realstock/company/sh600519/nc.shtml) <br>
- [Sina quote API batch example](https://hq.sinajs.cn/list=sh600519,sz300750,sh600036) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and formatted quote tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl for direct quote API calls; stock names returned by the API may require GBK-aware decoding.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
