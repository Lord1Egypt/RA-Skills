## Description:

Provides A-share real-time quote lookup, minute-level volume analysis, main-capital movement signals, limit-up context, and local portfolio profit/loss tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[litiao1224](https://clawhub.ai/user/litiao1224)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to query Chinese A-share market data, inspect minute-volume patterns, evaluate position profit and loss, and manage a local portfolio record.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Portfolio commands store stock codes, costs, quantities, and timestamps in a local JSON file.

Mitigation: Review the saved data before use on shared machines and tighten local file permissions when needed.

Risk: Removing or updating a portfolio entry changes the saved local portfolio file immediately.

Mitigation: Confirm the target stock code and keep backups before running update or remove commands.

Risk: Market analysis depends on external Sina Finance endpoints and may return stale or unavailable data outside normal trading conditions.

Mitigation: Treat outputs as informational and verify important trading decisions against authoritative market sources.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/litiao1224/skills/a-stock-analysis-litiao)
- [Publisher profile](https://clawhub.ai/user/litiao1224)
- [Sina Finance](https://finance.sina.com.cn)
- [Sina realtime quote endpoint](https://hq.sinajs.cn/list={codes_str})

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Analysis, Files]

**Output Format:** [Console text or JSON from Python command-line scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Portfolio commands read and write local JSON at ~/.clawdbot/skills/a-stock-analysis/portfolio.json.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
