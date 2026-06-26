## Description: <br>
Aicoin Trading helps an agent inspect centralized crypto exchange markets and prepare or execute spot and perpetual futures trading actions through the bundled Node.js and CCXT command-line tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[procaross](https://clawhub.ai/user/procaross) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to query centralized crypto exchange data, review balances and positions, and prepare or execute CEX spot or perpetual futures actions. It is intended for environments where the user deliberately grants exchange API access and reviews high-risk trading operations before execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access live crypto exchange accounts and may place, cancel, close, or modify leveraged trades when provided with exchange API credentials. <br>
Mitigation: Use least-privilege API keys with withdrawals disabled, restrict credentials to intended exchanges, and require explicit user confirmation before every order, cancellation, close, leverage, margin, or transfer action. <br>
Risk: Server security evidence reports under-disclosed paths that can place or cancel live leveraged trades without the documented confirmation flow. <br>
Mitigation: Review and restrict the auto-trade and trade.mjs paths before use, and monitor executions so direct confirmed trading calls cannot run without user approval. <br>
Risk: The artifact checks local environment files for credentials and includes broker or referral behavior. <br>
Mitigation: Review local .env access and broker/referral behavior before providing credentials, and disclose the behavior to users who operate the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/procaross/aicoin-trading) <br>
- [AiCoin OpenData](https://www.aicoin.com/opendata) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and JSON-formatted command output with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include live account, order, market, and risk-preview details when connected to exchange credentials.] <br>

## Skill Version(s): <br>
3.7.3 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
