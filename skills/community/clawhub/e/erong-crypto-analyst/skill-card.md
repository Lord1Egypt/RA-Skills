## Description: <br>
A cryptocurrency analysis skill that integrates OKX, Binance, and AKShare data for market lookup, technical analysis, trading signals, capital flow, position sizing, DCA planning, and risk calculations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[erongcao](https://clawhub.ai/user/erongcao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and crypto market participants use this skill to collect exchange data, run technical and sentiment analysis, compare exchange prices, size positions, plan DCA schedules, and generate structured trading-risk guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access private OKX account-balance data when API credentials are configured. <br>
Mitigation: Use only read-only OKX API credentials with no trading or withdrawal permissions, and avoid the balance checker unless private account-balance output is intended. <br>
Risk: Normal OKX analysis can run hard-coded helper scripts from local absolute paths for news collection. <br>
Mitigation: Run OKX analysis with --no-news unless the referenced local helper scripts have been inspected and are trusted. <br>
Risk: The security verdict is suspicious because private account access and hard-coded local helper execution are under-disclosed. <br>
Mitigation: Review the artifact before installing, scan it before deployment, and limit execution to trusted environments. <br>


## Reference(s): <br>
- [Crypto Analyst ClawHub page](https://clawhub.ai/erongcao/erong-crypto-analyst) <br>
- [Publisher profile](https://clawhub.ai/user/erongcao) <br>
- [OKX API endpoint](https://www.okx.com) <br>
- [Binance market data endpoint](https://data-api.binance.vision) <br>
- [Binance futures endpoint](https://fapi.binance.com) <br>
- [Alternative.me Fear and Greed API](https://api.alternative.me/fng/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and terminal-oriented text with inline shell commands and structured analysis summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call public market-data APIs and, when configured, read-only OKX account APIs; results depend on live external data availability.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
