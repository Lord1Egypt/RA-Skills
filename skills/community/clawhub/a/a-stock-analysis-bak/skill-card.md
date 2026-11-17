## Description:

Provides A-share real-time quote lookup, intraday volume distribution analysis, major-money signal interpretation, limit-up order checks, and local portfolio profit-and-loss management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[litiao1224](https://clawhub.ai/user/litiao1224)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to query Shanghai, Shenzhen, and Beijing Stock Exchange A-share quotes, inspect intraday volume patterns, and manage a small local portfolio file for position and profit-and-loss analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Portfolio positions, cost basis, quantities, and timestamps are stored in a plaintext local file.

Mitigation: Use this skill only on trusted machines, restrict permissions on ~/.clawdbot/skills/a-stock-analysis and portfolio.json, and avoid storing sensitive portfolio details on shared systems.

Risk: Live analysis sends queried stock codes to Sina Finance endpoints.

Mitigation: Treat queried stock symbols as externally disclosed to the market-data provider and avoid querying codes that reveal sensitive trading intent.

Risk: Removing or updating positions changes the local portfolio record.

Mitigation: Keep backups of portfolio.json when portfolio history matters, especially before using remove or update commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/litiao1224/skills/a-stock-analysis-bak)
- [Publisher profile](https://clawhub.ai/user/litiao1224)
- [Sina Finance](https://finance.sina.com.cn)
- [Sina realtime quote endpoint](https://hq.sinajs.cn/list={codes_str})

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Files, Guidance]

**Output Format:** [Plain text analysis or JSON results, with shell command examples for running the bundled Python scripts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Portfolio commands read and write a local JSON file at ~/.clawdbot/skills/a-stock-analysis/portfolio.json.]

## Skill Version(s):

1.0.0 (source: release evidence and _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
