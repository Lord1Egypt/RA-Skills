## Description:

Resolve a China A-share stock name or code with a Node.js helper, fetch daily historical OHLCV bars from Eastmoney HTTP APIs, and archive the results as local JSON files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenchunjiekk](https://clawhub.ai/user/chenchunjiekk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to resolve China A-share identifiers, fetch daily historical market bars from Eastmoney, and save raw JSON archives for downstream data workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes outbound HTTP requests to Eastmoney services.

Mitigation: Install and run it only where Eastmoney network access is allowed, or constrain egress with destination allowlists.

Risk: The skill writes cached symbol lists and raw market-data JSON files into the working repository.

Mitigation: Run it from a workspace where data/cache and data/raw/eastmoney/daily_history writes are expected, and review generated files before committing or sharing them.

## Reference(s):

- [LobsterClaw Workflow Notes](references/lobsterclaw-workflow.md)
- [Eastmoney historical kline API endpoint](https://push2his.eastmoney.com/api/qt/stock/kline/get)
- [Eastmoney quote site](https://quote.eastmoney.com/)
- [ClawHub skill page](https://clawhub.ai/chenchunjiekk/skills/fetch-stock-daily)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Files, Guidance]

**Output Format:** [Markdown with shell commands and JSON summaries; generated archives are JSON files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Archives rows under data/raw/eastmoney/daily_history and may cache symbol lists under data/cache/eastmoney.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
