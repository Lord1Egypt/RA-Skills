## Description: <br>
Looks up cryptocurrency prices and history, generates trend charts and weekly reports, and can send reports by email. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cscsxx606](https://clawhub.ai/user/cscsxx606) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to query current and historical cryptocurrency market data, generate chart-backed summaries, and configure optional recurring email reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Review before execution as proposals could introduce incorrect or misleading guidance into skills. <br>
Mitigation: Review and scan skill before deployment. <br>

## Reference(s): <br>
- [Crypto Price Pro on ClawHub](https://clawhub.ai/cscsxx606/crypto-price-pro) <br>
- [CoinGecko](https://www.coingecko.com/) <br>
- [CoinGecko simple price API](https://api.coingecko.com/api/v3/simple/price) <br>
- [CoinGecko market chart API](https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands; scripts emit terminal text, PNG chart files, and HTML email reports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses CoinGecko market data, optional matplotlib chart generation, and optional SMTP email delivery configured with environment variables.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
