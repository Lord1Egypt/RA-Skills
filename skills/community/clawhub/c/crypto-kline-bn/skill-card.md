## Description: <br>
Collects cryptocurrency candlestick data for BTC and other Binance-supported trading pairs across multiple intervals, with historical range and proxy options. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[u91win](https://clawhub.ai/user/u91win) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to fetch public Binance kline market data for selected symbols and intervals, then inspect or store the results locally for analysis workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Network requests may fail or expose traffic when routed through an untrusted proxy. <br>
Mitigation: Use a trusted proxy or disable the default proxy before running the collector. <br>
Risk: Large date ranges can create substantial local downloads and database writes. <br>
Mitigation: Confirm the symbol, interval, date range, and a dedicated database path before collection. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/u91win/crypto-kline-bn) <br>
- [Artifact documentation](artifact/SKILL.md) <br>
- [Python Binance kline collector](artifact/scripts/crypto-kline.py) <br>
- [Node.js Binance kline collector](artifact/scripts/binance-kline.js) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown guidance with bash commands and Python/Node.js scripts; runtime output includes terminal text and local SQLite database files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access to Binance API; supports optional proxy configuration, symbol and interval parameters, date ranges, and database path selection.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
