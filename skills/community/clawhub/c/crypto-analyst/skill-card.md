## Description: <br>
Crypto Analyst provides cryptocurrency market analysis across OKX and Binance, including price checks, technical indicators, trading signals, fund-flow checks, position sizing, DCA planning, and risk calculations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[erongcao](https://clawhub.ai/user/erongcao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to gather crypto market data, run technical and sentiment checks, compare exchanges, and produce trading-oriented analysis with position sizing and DCA calculations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security scan reports that OKX account credentials are used for private balance access. <br>
Mitigation: Use read-only OKX API keys, disable trading and withdrawals, and avoid storing powerful exchange credentials in the skill directory. <br>
Risk: The security scan reports default execution of hard-coded local helper scripts for news collection. <br>
Mitigation: Run OKX analysis with news disabled unless the local crypto-monitor and wire-news-aggregator helper scripts are present and trusted. <br>
Risk: The security scan verdict is suspicious and recommends review before installation. <br>
Mitigation: Review and scan the artifact before deployment, with attention to credential handling and local helper-script execution. <br>


## Reference(s): <br>
- [Crypto Analyst on ClawHub](https://clawhub.ai/erongcao/crypto-analyst) <br>
- [OKX API](https://www.okx.com) <br>
- [Binance Public Market Data API](https://data-api.binance.vision) <br>
- [Binance US API](https://api.binance.us) <br>
- [Binance Futures API](https://fapi.binance.com) <br>
- [Alternative.me Fear and Greed API](https://api.alternative.me/fng/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown analysis with inline shell commands and text reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call public market-data APIs and OKX account APIs when credentials are configured.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
