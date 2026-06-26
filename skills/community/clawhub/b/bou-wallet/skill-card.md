## Description: <br>
Guides an external agent with an existing Bank of Universe agent API key to call the backend with curl for x402 pay-and-call requests, agent wallet/profile inspection, and Hyperliquid account and trading operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0xcipher0](https://clawhub.ai/user/0xcipher0) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External agents and developers use this skill to operate the Bank of Universe backend through an existing bearer key, including x402-paid upstream calls, wallet/profile checks, market data, and Hyperliquid trading workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill instructs an agent to use a bearer key for payments, trades, leverage changes, transfers, and withdrawals. <br>
Mitigation: Use a dedicated limited agent key when available, keep the key secret, start with read-only endpoints, and require explicit approval before executing any payment, trade, cancel-all, leverage, transfer, or withdrawal request. <br>
Risk: The pay-and-call flow can spend USDC on upstream x402-protected URLs. <br>
Mitigation: Verify the backend URL, the upstream destination, and the expected payment before each request; rely on the documented backend payment limit as a backstop, not as the only control. <br>


## Reference(s): <br>
- [Bou Wallet on ClawHub](https://clawhub.ai/0xcipher0/bou-wallet) <br>
- [Bank of Universe App](https://app.bankofuniverse.org/) <br>
- [Bank of Universe API](https://api.bankofuniverse.org/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with curl command examples and JSON request/response shapes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires BASE_URL and a secret AGENT_KEY bearer token; generated commands can initiate payments, trades, transfers, or withdrawals when executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
