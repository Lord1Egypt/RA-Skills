## Description: <br>
Fetches public Huobi real-time market data and historical K-line data for major cryptocurrency spot trading pairs with selectable intervals and record counts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[u91win](https://clawhub.ai/user/u91win) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and market-data users use this skill to query recent Huobi K-line candles and real-time market data for cryptocurrency pairs such as BTC, ETH, and SOL. The results support informational market review and agent workflows that need public price and volume history. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The script contacts Huobi's public API and depends on that service's availability and returned market data. <br>
Mitigation: Use the results as informational data, handle request failures, and confirm important values against an authoritative market-data source before relying on them. <br>
Risk: Cryptocurrency market data may be mistaken for trading guidance. <br>
Mitigation: Present the output as market information only and avoid treating it as financial advice or an instruction to place trades. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/u91win/crypto-kline-data) <br>
- [Publisher profile](https://clawhub.ai/user/u91win) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, API calls, Guidance] <br>
**Output Format:** [Markdown guidance and terminal text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a local Node.js script to request public Huobi market data; requested record count is capped at 2000.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
