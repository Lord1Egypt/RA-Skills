## Description: <br>
Binance Onchain Pay helps agents buy crypto with fiat or send crypto to on-chain wallet addresses through Binance Onchain-Pay Open API workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dexploarer](https://clawhub.ai/user/dexploarer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to prepare and execute Binance Onchain-Pay API calls for fiat-to-crypto purchases, external wallet sends, order monitoring, payment method discovery, network lookup, and merchant payment flows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can help initiate high-impact crypto purchase, transfer, and pre-order workflows using stored credentials. <br>
Mitigation: Use test or low-limit credentials and require explicit approval of the account, endpoint, sanitized payload, amount, asset, address, network, and action before any order or transfer-related call. <br>
Risk: Private keys, API keys, and local credential paths may be exposed if request details are shown too broadly. <br>
Mitigation: Keep PEM contents and paths private, mask API keys, and send credentials only to the configured Binance Onchain-Pay base URL. <br>


## Reference(s): <br>
- [Binance Onchain-Pay Open API Authentication](references/authentication.md) <br>
- [ClawHub skill page](https://clawhub.ai/dexploarer/binance-onchain-pay) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, API calls, configuration, text] <br>
**Output Format:** [Markdown guidance with shell commands and readable API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use stored local credentials to sign POST requests and display sanitized request or response details.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
