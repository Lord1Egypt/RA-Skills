## Description:

Use when the user wants to sell or buy an NFT on Element, create or accept a bid or offer, query public collection orders or account orders, cancel an Element order, get the configured trading wallet address, or use a supported custom payment token on a supported Element EVM network.

This skill is ready for commercial/non-commercial use.

## Publisher:

[element-som](https://clawhub.ai/user/element-som)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to manage Element Market NFT trading workflows, including listings, purchases, offers, cancellations, order queries, and wallet-address lookup. It is intended for trading actions and order management rather than collection analytics or portfolio tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can sign high-impact NFT trading transactions and approvals that may move assets or grant lasting marketplace permissions.

Mitigation: Use a dedicated low-value wallet, preview every state-changing action, require explicit confirmation, and verify transaction details in an external wallet or explorer before funding the wallet.

Risk: Remote marketplace calldata may be signed with insufficient local validation.

Mitigation: Use only exact order objects returned by the query workflow, avoid hand-reconstructed order data, and confirm network, collection, token, payment token, price, and quantity before execution.

Risk: Private-key exposure would compromise the configured trading wallet.

Mitigation: Keep the private key in the local environment only; never ask users to paste it into chat and never echo it in responses.

## Reference(s):

- [Element NFT Trader on ClawHub](https://clawhub.ai/element-som/skills/element-nft-trader)
- [Publisher Profile](https://clawhub.ai/user/element-som)
- [Project Homepage](https://github.com/element-som/element-skills)
- [Payment Tokens](references/payment-tokens.md)
- [Sell](references/sell.md)
- [Buy](references/buy.md)
- [Offer](references/offer.md)
- [Accept Offer](references/accept-offer.md)
- [Query Orders](references/query-orders.md)
- [Query Account Orders](references/query-account-orders.md)
- [Cancel](references/cancel.md)
- [Get Wallet Address](references/get-address.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with JSON payloads and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May execute read-only queries or confirmed state-changing blockchain transaction commands through the bundled Node.js executor.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
