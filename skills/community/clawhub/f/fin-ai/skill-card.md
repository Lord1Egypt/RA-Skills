## Description:

Fin Ai helps agents manage Chinese-language investment portfolio workflows by syncing holdings, recalculating portfolio results, and generating daily snapshots and history from screenshots, CSVs, brokerage exports, or holdings-like JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaotaoguo](https://clawhub.ai/user/xiaotaoguo)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to keep portfolio holdings as the source of truth, preview updates, refresh market-aware analysis, review warnings, and persist confirmed daily snapshot/history outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can write portfolio holdings, snapshots, history, and settings data.

Mitigation: Install only when the portfolio directory and JSON inputs are trusted, use preview mode first, inspect the summary and warnings, and require explicit confirmation before persistent writes.

Risk: Market-data lookup can make network requests and may accept configurable endpoint or proxy values.

Mitigation: Use trusted network settings, review config.json before analysis, and restrict yahoo_base and proxy values to approved endpoints.

Risk: Malformed dates or untrusted holdings/snapshot files can produce misleading analysis or unsafe writes.

Mitigation: Validate dates as YYYY-MM-DD and review holdings, market context, and snapshot files before using direct write scripts.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/xiaotaoguo/skills/fin-ai)
- [Holdings Schema](references/schema-holdings.md)
- [Lot Ledger Schema](references/schema-lots.md)
- [Snapshot Schema](references/schema-snapshot.md)
- [Workflow Contracts](references/workflow-contracts.md)
- [Yahoo Finance Chart Endpoint](https://query1.finance.yahoo.com/v8/finance/chart)
- [Eastmoney Fund Endpoint](https://fund.eastmoney.com/pingzhongdata/{code}.js)
- [FundGZ Endpoint](https://fundgz.1234567.com.cn/js/{code}.js)
- [Stooq Quote Endpoint](https://stooq.com/q/l/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands; scripts may produce JSON portfolio snapshots and CSV history rows.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preview mode is the normal posture; persistent writes require explicit user confirmation.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
