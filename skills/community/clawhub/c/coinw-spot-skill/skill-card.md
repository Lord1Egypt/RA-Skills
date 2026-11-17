## Description:

Coinw Spot Skill gives agents access to CoinW Spot REST API workflows for market data, order placement and cancellation, order queries, account balances, and asset transfers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[connectcoinw](https://clawhub.ai/user/connectcoinw)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to connect an agent to CoinW spot trading workflows, including retrieving market data, checking account balances, placing or cancelling orders, and transferring assets between spot and funding accounts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide private CoinW Spot actions including order placement, order cancellation, and asset transfer.

Mitigation: Require explicit user confirmation before submitting orders, cancellations, or transfers, and show the operation, pair, amount, price, account direction, and expected endpoint before execution.

Risk: The skill requires CoinW API and secret keys for private endpoints.

Mitigation: Use least-privilege API keys, avoid withdrawal permission unless required, enable IP allowlisting, store secrets only in approved credential storage, and redact credentials, signatures, commands, and logs before sharing.

Risk: Incorrect signing, missing permissions, or API rate limits can cause failed or repeated requests.

Mitigation: Follow the Spot MD5 uppercase signing process, verify API permissions before account-changing operations, and apply request throttling with retry behavior that stops before repeated order attempts.

Risk: A returned order identifier does not prove trade execution.

Mitigation: Query order status or order details after submitting an order and present execution state separately from request acceptance.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/connectcoinw/skills/coinw-spot-skill)
- [connectcoinw publisher profile](https://clawhub.ai/user/connectcoinw)
- [Authentication](artifact/references/Authentication.md)
- [API Key Creation Steps](artifact/references/api-key-creation-steps.md)
- [Error Code Explanation](artifact/references/error-codes.md)
- [Notes](artifact/references/notes.md)
- [CoinW Spot trading pair information API](https://www.coinw.com/api-doc/spot-trading/market/get-trading-pair-information)
- [CoinW Spot place order API](https://www.coinw.com/api-doc/spot-trading/trade/place-order)
- [CoinW Spot cancel order API](https://www.coinw.com/api-doc/spot-trading/trade/cancel-order)
- [CoinW Spot account balance API](https://www.coinw.com/api-doc/spot-trading/account/get-spot-account-balance)
- [CoinW Spot asset transfer API](https://www.coinw.com/api-doc/spot-trading/account/transfer-assets)

## Skill Output:

**Output Type(s):** [guidance, shell commands, code, configuration, markdown]

**Output Format:** [Markdown with REST endpoint tables, credential guidance, and inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include signed CoinW REST request examples and operational guidance for public and private Spot endpoints.]

## Skill Version(s):

1.5.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
