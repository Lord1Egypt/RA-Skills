## Description:

Provides real-time A-share quotes, intraday volume distribution analysis, main fund movement signals, limit-up order context, and local portfolio profit/loss management for Shanghai, Shenzhen, and Beijing Stock Exchange stocks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[litiao1224](https://clawhub.ai/user/litiao1224)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to query A-share market data, inspect minute-level volume patterns, identify heuristic trading signals, and manage locally stored stock positions with profit/loss analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Portfolio commands store tracked holdings locally at ~/.clawdbot/skills/a-stock-analysis/portfolio.json.

Mitigation: Use the skill only where local storage of holdings is acceptable, and tighten file and directory permissions on shared machines.

Risk: Market-data commands send requested stock codes to Sina Finance endpoints.

Mitigation: Run the skill only when sharing queried stock codes with those market-data services is acceptable.

Risk: The trading signals are heuristic interpretations of market data and can be incomplete or misleading.

Mitigation: Treat the output as informational analysis and review against independent sources before making investment decisions.

## Reference(s):

- [ClawHub skill release page](https://clawhub.ai/litiao1224/skills/a-stock-analysis-conflict)
- [Sina Finance](https://finance.sina.com.cn)
- [Sina real-time quote endpoint](https://hq.sinajs.cn)
- [Sina minute K-line endpoint](https://quotes.sina.cn)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Console text or JSON produced by Python CLI scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local portfolio data under ~/.clawdbot/skills/a-stock-analysis/portfolio.json when portfolio commands are used.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
