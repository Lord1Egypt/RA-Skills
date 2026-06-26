## Description: <br>
Resolves a China A-share stock name or code, fetches daily historical OHLCV bars from Eastmoney HTTP APIs, and archives the result as local JSON files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chenchunjiekk](https://clawhub.ai/user/chenchunjiekk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agents use this skill to resolve China A-share stock inputs and export daily market-history JSON for downstream analysis or archival workflows. <br>

### Deployment Geography for Use: <br>
Global, for workflows that need China A-share market data. <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes outbound requests to Eastmoney and writes JSON archives into the workspace. <br>
Mitigation: Use only in environments where those network requests are allowed, and review or constrain the output directory before execution. <br>
Risk: Fetched market data may be incomplete, stale, or unsuitable for trading decisions. <br>
Mitigation: Treat the output as informational data and validate it against authoritative sources before financial reporting or investment use. <br>


## Reference(s): <br>
- [LobsterClaw Workflow Notes](references/lobsterclaw-workflow.md) <br>
- [Eastmoney Historical Kline API](https://push2his.eastmoney.com/api/qt/stock/kline/get) <br>
- [Eastmoney Quote Site](https://quote.eastmoney.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown response with the script command context, a JSON summary, and a saved local JSON archive.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The summary reports the resolved symbol, row count, requested date window, trade-date bounds, and output path.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
