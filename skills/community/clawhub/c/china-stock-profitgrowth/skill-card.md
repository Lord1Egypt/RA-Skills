## Description:

Screens China A-share stocks for a public-source approximation of net profit growth using Eastmoney public market data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luyao-inc](https://clawhub.ai/user/luyao-inc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to run a local Python stock-screening helper for A-share profit-growth candidates and receive a JSON-ranked list for further review. Outputs are approximate and should not be treated as investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Stock-screening outputs are approximate and may be incomplete or misleading for financial decisions.

Mitigation: Treat results as a starting point only and independently verify candidates before taking investment action.

Risk: The skill runs a local Python script that contacts Eastmoney public quote APIs.

Mitigation: Review the script and allow network execution only in environments where this data access is acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/luyao-inc/skills/china-stock-profitgrowth)
- [README.md](README.md)
- [SKILL.md](SKILL.md)
- [Eastmoney public quote API](https://push2.eastmoney.com/api/qt/clist/get)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [Markdown instructions with shell command usage and JSON results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [JSON includes ok, strategy_type, stocks, and message; stock data comes from public market APIs.]

## Skill Version(s):

2.0.0 (source: release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
