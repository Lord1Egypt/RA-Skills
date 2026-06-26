## Description: <br>
Specialized A-share stock data collector that automatically fetches and stores daily, weekly, and monthly historical K-line data for all A-share stocks in a SQLite database. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiyunnet](https://clawhub.ai/user/xiyunnet) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agents use this skill to initialize and maintain a local Chinese A-share market-data store for quantitative analysis and scheduled updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Hard-coded local data paths may write files or fail unexpectedly on systems that do not use the documented D:\xistock layout. <br>
Mitigation: Review and, if needed, change the data path before running initialization or fetch scripts. <br>
Risk: Fetchers make public market-data API requests and may hit rate limits or collect more data than intended. <br>
Mitigation: Start with small --limit values, run in non-trading hours when appropriate, and monitor network/API behavior. <br>
Risk: Reset and repair commands modify the local SQLite database and fetch timestamps. <br>
Mitigation: Back up stock.db before reset or repair commands and inspect status output before bulk operations. <br>
Risk: Generated cron configuration can trigger recurring automated updates. <br>
Mitigation: Enable scheduled jobs only when recurring market-data updates are intended and review the generated schedule. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/xiyunnet/a-stock-get) <br>
- [AkShare Documentation](https://akshare.readthedocs.io/) <br>
- [SQLite Python Tutorial](https://docs.python.org/3/library/sqlite3.html) <br>
- [Tencent Finance K-line endpoint](https://proxy.finance.qq.com/ifzqgtimg/appstock/app/newfqkline/get) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Configuration, Files] <br>
**Output Format:** [Markdown guidance with bash command examples and generated local SQLite/text data files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local filesystem state, public market-data API traffic, and optional scheduled jobs; no API keys were detected.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
