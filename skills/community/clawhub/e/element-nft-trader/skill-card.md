## Description: <br>
Element NFT Trader helps agents manage Element Market NFT trading workflows, including sell orders, purchases, offers, order queries, cancellations, wallet address lookup, and supported custom payment-token use on Element EVM networks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[element-som](https://clawhub.ai/user/element-som) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to operate Element Market NFT trading workflows from an agent, including querying orders, preparing transactions, and executing sell, buy, offer, accept-offer, and cancel operations after explicit confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can sign and broadcast real blockchain transactions from a configured private-key wallet. <br>
Mitigation: Use a dedicated low-value wallet, require explicit confirmation for state-changing operations, and keep the private key out of chat. <br>
Risk: The skill can automatically grant broad token or NFT approvals during sell, buy, offer, and accept-offer flows. <br>
Mitigation: Review approval transactions before submission, verify the approved token or collection and spender address, and revoke approvals after use when they are no longer needed. <br>
Risk: Incorrect chain, collection, order, or payment-token assumptions can change execution scope or cause unintended trades. <br>
Mitigation: Require the network and all operation-specific parameters before execution, use the matching reference file for payload construction, and do not guess unsupported ERC20 tokens or order identifiers. <br>


## Reference(s): <br>
- [Element NFT Trader skill page](https://clawhub.ai/element-som/element-nft-trader) <br>
- [Element Skills repository](https://github.com/element-som/element-skills) <br>
- [Element API keys](https://element.market/apikeys) <br>
- [Element Market](https://element.market) <br>
- [Accept Offer](references/accept-offer.md) <br>
- [Buy](references/buy.md) <br>
- [Cancel](references/cancel.md) <br>
- [Get Wallet Address](references/get-address.md) <br>
- [Offer](references/offer.md) <br>
- [Payment Tokens](references/payment-tokens.md) <br>
- [Query Account Orders](references/query-account-orders.md) <br>
- [Query Orders](references/query-orders.md) <br>
- [Sell](references/sell.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON payloads and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include transaction previews, structured operation results, explorer links, order tables, wallet addresses, and guidance for required confirmations.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
