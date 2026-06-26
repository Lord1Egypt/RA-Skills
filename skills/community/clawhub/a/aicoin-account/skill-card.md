## Description: <br>
Helps agents query crypto exchange account state, order and trade history, AiCoin data-tier status, API-key setup, exchange registration links, transfers, order cancellation, and trading parameter changes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[procaross](https://clawhub.ai/user/procaross) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and their agents use this skill to inspect crypto exchange balances, positions, orders, and trades; configure AiCoin data API access; check data-tier availability; and run exchange account workflows such as registration, transfers, cancellation, leverage, and margin settings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can exercise live exchange-account authority, including trading, order cancellation, leverage, margin, and fund-transfer actions. <br>
Mitigation: Install only when an agent is intended to have this authority; use tightly scoped API keys, avoid withdrawal permissions, and require clear human confirmation before transfer, order, leverage, margin, or cancellation requests. <br>
Risk: The skill requires sensitive AiCoin and exchange API credentials and can read local .env files. <br>
Mitigation: Configure credentials only through the intended environment mechanism, keep secrets out of chat output, review .env file locations before use, and rotate keys if they may have been exposed. <br>
Risk: The server security summary says the account-management/read-only framing understates the implemented live trading and transfer powers. <br>
Mitigation: Review the command surface and security guidance before deployment, and do not rely on read-only descriptions when deciding what permissions to grant. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/procaross/aicoin-account) <br>
- [AiCoin OpenData](https://www.aicoin.com/opendata) <br>
- [Publisher profile](https://clawhub.ai/user/procaross) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read local environment variables and .env files for AiCoin and exchange API credentials.] <br>

## Skill Version(s): <br>
2.0.0 (source: package.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
