## Description: <br>
Access crypto data, monitor portfolios, detect scams, and navigate exchanges with real-time APIs and security tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, analysts, and crypto users use this skill to retrieve market and on-chain data, monitor portfolios, perform basic calculations, and evaluate scam indicators without receiving investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Crypto market or portfolio output may be mistaken for financial advice. <br>
Mitigation: Keep responses informational, avoid buy/sell/hold recommendations, include the skill's investment disclaimer when investment topics arise, and direct users to qualified professionals for personal decisions. <br>
Risk: Prices, gas fees, and contract status can change quickly or differ across providers. <br>
Mitigation: Verify outputs against official APIs or chain explorers, show source context when possible, and avoid presenting real-time data as guaranteed or final. <br>
Risk: Users may expose wallet secrets, exchange credentials, seed phrases, or trading authorization while asking for help. <br>
Mitigation: Do not request or process secrets, credentials, seed phrases, or authorization to trade; limit assistance to public data and user-provided non-secret context. <br>
Risk: Scam checks can be overinterpreted as a statement that a token or contract is safe. <br>
Mitigation: Present scam and contract findings as technical indicators only, state that no crypto asset is risk-free, and encourage independent review before interacting with contracts. <br>


## Reference(s): <br>
- [Crypto Tools on ClawHub](https://clawhub.ai/ivangdavila/crypto-tools) <br>
- [Crypto Data Sources](sources.md) <br>
- [Crypto Security & Scam Detection](security.md) <br>
- [Crypto Utilities & Calculations](tools.md) <br>
- [CoinGecko API price endpoint](https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd,eur) <br>
- [DefiLlama protocol data endpoint](https://api.llama.fi/protocols) <br>
- [Etherscan gas oracle endpoint](https://api.etherscan.io/api?module=gastracker&action=gasoracle) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API Calls, Shell commands, Code, Markdown, Configuration] <br>
**Output Format:** [Markdown with inline code blocks, API examples, formulas, and CSV examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are informational and should be verified against primary sources before decisions or transactions.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
