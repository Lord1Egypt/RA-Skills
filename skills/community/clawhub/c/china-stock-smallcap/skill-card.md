## Description:

小市值选股（纯 OpenClaw 公开源版）：基于东财公开行情做小市值近似筛选。

This skill is ready for commercial/non-commercial use.

## Publisher:

[luyao-inc](https://clawhub.ai/user/luyao-inc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and market-analysis users can run this skill to retrieve an informational, public-data-based screen of China A-share small-cap stocks and related quote fields. The output is an approximation and is not investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The stock screen is an approximate informational result and may be misleading if treated as financial advice.

Mitigation: Use the output only as a starting point for analysis, verify market data independently, and do not treat results as investment advice.

Risk: The selector depends on the availability and response shape of the Eastmoney public quote API.

Mitigation: Review command results for errors or missing fields and update the selector if the upstream API changes.

Risk: The documented command path may not match the packaged artifact layout.

Mitigation: Confirm the installed skill exposes the selector at the documented path before relying on the command.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/luyao-inc/skills/china-stock-smallcap)
- [Eastmoney public quote API](https://push2.eastmoney.com/api/qt/clist/get)

## Skill Output:

**Output Type(s):** [Text, Shell commands, JSON, Guidance]

**Output Format:** [JSON from a command-line Python selector, with agent-facing guidance in Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns ranked stock entries with symbol, name, price, percent change, turnover, market cap, main net inflow, P/E, P/B, raw source fields, status, strategy type, and message.]

## Skill Version(s):

2.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
