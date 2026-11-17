## Description:

Filters a China A-share stock candidate pool using Eastmoney public real-time main net inflow data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luyao-inc](https://clawhub.ai/user/luyao-inc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and market-analysis agents use this skill to run a Python stock-screening helper and inspect candidate A-share stocks ranked by public real-time main net inflow. The output is for reference and should not be treated as investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Financial screening output can be incomplete, delayed, or unsuitable for a trading decision.

Mitigation: Verify market data independently and do not treat the skill output as investment advice.

Risk: The skill depends on an external public market-data endpoint that may change, fail, or return unavailable fields.

Mitigation: Check the returned ok status, row_count, and columns before relying on the result.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/luyao-inc/skills/china-stock-main-force)
- [Publisher profile](https://clawhub.ai/user/luyao-inc)
- [Eastmoney public quote API endpoint](https://push2.eastmoney.com/api/qt/clist/get)

## Skill Output:

**Output Type(s):** [json, shell commands, guidance]

**Output Format:** [JSON from a Python command, usually discussed in Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Rows include symbol, name, price, percent change, main net inflow, market cap, turnover, PE, and PB when available.]

## Skill Version(s):

2.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
