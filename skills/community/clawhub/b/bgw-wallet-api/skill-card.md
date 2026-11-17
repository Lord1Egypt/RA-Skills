## Description:

Interact with Bitget Wallet API for crypto market data, token information, swap quotes, order workflows, and token security audits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[karryzhang](https://clawhub.ai/user/karryzhang)

### License/Terms of Use:


## Use Case:

External users, developers, traders, and agent builders use this skill to query Bitget Wallet market data, assess token risk, generate swap quotes, create unsigned transaction or order data, submit signed orders, and track order status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes wallet signing and transaction submission paths that can move funds or expose private keys.

Mitigation: Use a dedicated low-value wallet, independently review transaction details before signing, and do not pass valuable wallet private keys on the command line.

Risk: The skill includes an update flow that references a mutable branch.

Mitigation: Review updates separately before installation, especially changes to endpoints, dependencies, credential handling, and signing behavior.

Risk: Swap and order workflows may expose users to token, slippage, liquidity, and execution risks.

Mitigation: Run token security checks, review quote and liquidity details, and require clear human confirmation before generating calldata, signing, or submitting orders.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/karryzhang/skills/bgw-wallet-api)
- [Publisher profile](https://clawhub.ai/user/karryzhang)
- [Bitget Wallet API documentation](https://web3.bitget.com/en/docs)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can produce authenticated API calls, unsigned transaction data, signed order payloads when a private key is supplied, and risk summaries for token or swap workflows.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
