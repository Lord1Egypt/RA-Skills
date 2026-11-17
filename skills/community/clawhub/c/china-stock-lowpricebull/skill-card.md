## Description:

Screens China A-share stocks with public Eastmoney market data for low-price candidates using approximate price movement and capital-inflow criteria.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luyao-inc](https://clawhub.ai/user/luyao-inc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and market analysts use this skill to run a Python-based China A-share stock screen and receive ranked JSON results for low-price public-market candidates. The output is informational and is not investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Approximate stock-screening results may be incomplete, stale, or misleading because the skill relies on a public third-party market-data endpoint.

Mitigation: Use results as informational screening output only, verify market data independently, and do not treat the output as investment advice or a trading signal.

Risk: The selection strategy is an open-source approximation and is not equivalent to proprietary WenCai formulas.

Mitigation: Review the disclosed criteria before use and confirm that the approximation fits the intended analysis workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/luyao-inc/skills/china-stock-lowpricebull)
- [Publisher profile](https://clawhub.ai/user/luyao-inc)
- [Artifact README](artifact/README.md)
- [Artifact skill definition](artifact/SKILL.md)
- [Eastmoney public quote API](https://push2.eastmoney.com/api/qt/clist/get)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [JSON results with concise Markdown usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns ranked stock objects with symbols, names, prices, movement, turnover, market capitalization, capital inflow, valuation fields, and raw public-data rows; results are approximate and informational.]

## Skill Version(s):

2.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
