## Description: <br>
Intellectia stock/crypto screener for Bullish/Bearish Tomorrow/Week/Month presets that calls /gateway/v1/stock/screener-list with no auth and summarizes results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xanxustan](https://clawhub.ai/user/xanxustan) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, analysts, and agent users use this skill to fetch stock or crypto screener candidates from Intellectia presets and summarize fields such as probability, profit, price, and change ratio. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Stock or crypto screener criteria may be sent to Intellectia's API. <br>
Mitigation: Avoid including personal financial details or private strategy notes in prompts. <br>
Risk: Returned market data may be mistaken for investment advice. <br>
Mitigation: Treat the screener output as informational and review independently before making financial decisions. <br>
Risk: The external API may rate limit or fail to return data. <br>
Mitigation: Use smaller page sizes and add retry or backoff behavior when automating requests. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xanxustan/ai-screener) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/xanxustan) <br>
- [Intellectia screener API endpoint](https://api.intellectia.ai/gateway/v1/stock/screener-list) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown summaries, tables, JSON snippets, cURL commands, and Python requests examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns informational market screener data from the disclosed Intellectia endpoint; no authentication is described.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
