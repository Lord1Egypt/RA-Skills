## Description:

Bou Wallet helps an external agent with an existing agent API key issue curl requests for x402 pay-and-call, wallet/profile inspection, and Hyperliquid read and trade operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xcipher0](https://clawhub.ai/user/0xcipher0)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and operators use this skill to guide authenticated curl calls against the Bank of Universe service for paid upstream requests, account inspection, market data, trading, leverage changes, transfers, and withdrawals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent API key may authorize spending, trading, transfers, or withdrawals.

Mitigation: Treat the key as a secret, avoid printing or storing it, prefer narrowly scoped keys, and require explicit user approval before write operations.

Risk: Changing BASE_URL can send the agent key to an untrusted backend.

Mitigation: Use https://api.bankofuniverse.org/ by default and only use a custom backend after independent trust verification.

Risk: Hyperliquid order, leverage, transfer, and withdrawal endpoints can create direct financial loss.

Mitigation: Verify market, side, size, price, leverage, destination, and balances before submitting any request.

Risk: x402 pay-and-call requests can spend USDC for upstream access.

Mitigation: Confirm the upstream URL, method, body, and expected cost before calling the paid endpoint.

## Reference(s):

- [Bou Wallet ClawHub listing](https://clawhub.ai/0xcipher0/skills/bou-wallet)
- [Bank of Universe app](https://app.bankofuniverse.org/)
- [Bank of Universe API](https://api.bankofuniverse.org/)
- [Bank of Universe x402 test service](https://skills.bankofuniverse.org/cos/crypto/chainlink/random)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with curl command examples and JSON request bodies]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes endpoint-specific request fields, authentication headers, setup guidance, and execution checks.]

## Skill Version(s):

1.0.0 (source: server release metadata and user changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
