## Description:

A-share ultra-short trading strategy guidance for identifying hot sectors, selecting leading stocks, and planning buy, sell, stop-loss, position, and review discipline for 1-2 day T+1 trading.

This skill is ready for commercial/non-commercial use.

## Publisher:

[c595390153-a11y](https://clawhub.ai/user/c595390153-a11y)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to structure A-share ultra-short trading analysis, including sector screening, leading-stock selection, trade planning, risk controls, and post-market review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may influence high-risk short-term stock-trading decisions using aggressive ultra-short trading assumptions.

Mitigation: Treat outputs as informational, verify market data independently, and make trading decisions outside the agent workflow.

Risk: Agent access to brokerage accounts or order placement could turn guidance into unintended financial action.

Mitigation: Keep brokerage access and trade execution behind separate explicit controls; do not grant this skill autonomous trading authority.

## Reference(s):

- [East Money concept sector fund flows](https://data.eastmoney.com/bkzj/gn.html)
- [CLS hot stocks](https://www.cls.cn/hot-stock)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or plain text trading-analysis guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Informational guidance only; no code execution, brokerage access, credential handling, persistence, or data exfiltration behavior is evidenced.]

## Skill Version(s):

1.0.0 (source: server release evidence, artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
