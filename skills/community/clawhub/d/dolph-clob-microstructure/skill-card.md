## Description: <br>
Analyzes Polymarket order book microstructure for inefficiencies and generates signals to trade fake breakouts and manage position sizing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[richducat](https://clawhub.ai/user/richducat) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and trading automation operators use this skill to scan active Polymarket markets, score order book microstructure, and produce actionable trading signals. In live mode it can place mean-reversion trades through SimmerClient using a configured API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live mode can place repeated financial trades automatically using a Simmer API key. <br>
Mitigation: Start in dry-run or simulation mode, use scoped and revocable credentials, and enable live execution only after independent strategy review. <br>
Risk: Cron execution can repeat trades without per-trade confirmation. <br>
Mitigation: Use conservative CLOB_TRADE_SIZE and CLOB_MAX_TRADES settings and avoid live cron execution unless repeated automated trading risk is accepted. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/richducat/dolph-clob-microstructure) <br>
- [Polymarket CLOB Order Book Endpoint](https://clob.polymarket.com/book) <br>
- [Polymarket Trades Data Endpoint](https://data-api.polymarket.com/trades) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, text, shell commands, configuration, API calls] <br>
**Output Format:** [Console logs and text summaries with generated trading signals] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SIMMER_API_KEY; defaults to dry-run unless started with --live.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
