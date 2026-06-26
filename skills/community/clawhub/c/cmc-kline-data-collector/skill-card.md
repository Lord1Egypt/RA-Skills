## Description: <br>
Fetches cryptocurrency K-line history from CoinMarketCap, computes EMA7, EMA30, and RSI14 indicators, and exports the results as JSON or CSV. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[HarrierDB](https://clawhub.ai/user/HarrierDB) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to collect recent crypto market OHLC data, calculate common technical indicators, and prepare machine-readable reports for downstream analysis or dashboards. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes recurring or on-demand network calls to fetch crypto market data. <br>
Mitigation: Run it only in environments where outbound access to CoinMarketCap is expected, and enable any cron schedule only when recurring collection is intended. <br>
Risk: The skill writes JSON and CSV exports to local paths that may overwrite or accumulate files. <br>
Mitigation: Use a dedicated output directory, review filenames before execution, and monitor generated reports for retention needs. <br>
Risk: Market data and calculated technical indicators can be incomplete, stale, or unsuitable for financial decisions without review. <br>
Mitigation: Treat outputs as data preparation artifacts and verify market data, timestamps, and indicator calculations before using them in analysis or decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/HarrierDB/cmc-kline-data-collector) <br>
- [CoinMarketCap data API endpoint](https://api.coinmarketcap.com/data-api/v3.1) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, csv, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with Python examples plus generated JSON or CSV data files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs include OHLC fields, EMA7, EMA30, RSI14, and MMDD dates for configured cryptocurrency symbols.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
