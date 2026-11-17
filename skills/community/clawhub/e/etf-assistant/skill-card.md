## Description:

ETF投资助理 / ETF Investment Assistant - 查询行情、筛选ETF、对比分析、定投计算。支持沪深300、创业板、科创50、纳指等主流ETF。

This skill is ready for commercial/non-commercial use.

## Publisher:

[franky0617](https://clawhub.ai/user/franky0617)

### License/Terms of Use:


## Use Case:

External users can use this skill to look up common ETF codes, query ETF quotes, search and compare ETF entries, and run simple dollar-cost averaging calculations. Its investment notes are for reference only and do not constitute financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The calculator can run unintended shell commands from crafted inputs.

Mitigation: Review or patch before installation; require strict numeric validation for amount and years and avoid evaluating user input in shell arithmetic or bc source.

Risk: Quote and comparison commands perform Yahoo Finance network lookups.

Mitigation: Keep network access visible to users and treat returned market data as external, time-sensitive information.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/franky0617/skills/etf-assistant)
- [Yahoo Finance chart endpoint](https://query1.finance.yahoo.com/v8/finance/chart/${code}.SS)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Terminal text output with command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Yahoo Finance network lookups for quote and comparison commands.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
