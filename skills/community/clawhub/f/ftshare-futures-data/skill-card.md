## Description: <br>
Provides agent-accessible futures contract lists, contract reference data, and OHLCV k-line history from market.ft.tech. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shawn92](https://clawhub.ai/user/shawn92) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to answer questions about futures contracts, map Chinese contract names or products to WIND symbols, retrieve contract base data, and fetch k-line or historical market data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs bundled Python scripts and makes outbound HTTPS requests to market.ft.tech. <br>
Mitigation: Install and use it only in environments where agent-executed Python and outbound market-data requests to market.ft.tech are acceptable. <br>
Risk: Market-data answers depend on upstream service availability, coverage, and returned field semantics. <br>
Mitigation: Check returned JSON fields, empty result sets, and timestamps before relying on the data in analysis or decisions. <br>


## Reference(s): <br>
- [ClawHub skill release](https://clawhub.ai/shawn92/ftshare-futures-data) <br>
- [market.ft.tech futures data service](https://market.ft.tech) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, JSON, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON responses from the bundled Python entrypoint] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Routes requests through futures-lists, futures-base-data, and futures-kline sub-skills; responses depend on market.ft.tech availability and upstream data coverage.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
