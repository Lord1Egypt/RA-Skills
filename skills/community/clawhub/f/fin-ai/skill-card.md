## Description: <br>
Chinese-language portfolio management skill for syncing holdings, recalculating portfolio results from holdings, reviewing warnings, and generating daily snapshot/history outputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaotaoguo](https://clawhub.ai/user/xiaotaoguo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and portfolio-tracking users use this skill to update local investment holdings from screenshots, CSV files, broker exports, or holdings-like JSON, then recalculate portfolio summaries and persist snapshots after confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Portfolio holdings and financial symbols may be stored locally and copied into preview temporary folders. <br>
Mitigation: Use preview mode first, review the summary and warnings, and manually remove any portfolio-workflows-safe-run temporary folders that should not remain on disk. <br>
Risk: Ticker symbols may be sent to external market-data providers when market data is refreshed. <br>
Mitigation: Use an explicit market_context JSON when avoiding external lookups, and confirm writes only after reviewing the data sources and warnings. <br>
Risk: Confirmed writes update the real portfolio directory, including holdings, snapshots, and history outputs. <br>
Mitigation: Run without confirm-write for preview, then use confirmed writes only when the intended portfolio directory and generated summary have been reviewed. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/xiaotaoguo/fin-ai) <br>
- [Holdings Schema](references/schema-holdings.md) <br>
- [Lot Ledger Schema](references/schema-lots.md) <br>
- [Snapshot Schema](references/schema-snapshot.md) <br>
- [Workflow Contracts](references/workflow-contracts.md) <br>
- [Yahoo Finance chart endpoint](https://query1.finance.yahoo.com/v8/finance/chart) <br>
- [Eastmoney fund data endpoint](https://fund.eastmoney.com/pingzhongdata/{code}.js) <br>
- [Fundgz fund quote endpoint](https://fundgz.1234567.com.cn/js/{code}.js) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, JSON, Files] <br>
**Output Format:** [Markdown summaries with inline shell commands and JSON/file outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Preview mode summarizes portfolio totals, profit/loss, account groups, warnings, and whether real data will be written.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
