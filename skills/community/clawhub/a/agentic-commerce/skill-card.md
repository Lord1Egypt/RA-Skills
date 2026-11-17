## Description:

AI-powered shopping API for product search, purchase order creation, and crypto checkout with USDC on Solana or Base.

This skill is ready for commercial/non-commercial use.

## Publisher:

[purch-agent](https://clawhub.ai/user/purch-agent)

### License/Terms of Use:


## Use Case:

Developers building shopping assistants or commerce automations use this skill to search Amazon and Shopify products, create purchase orders, and guide or execute USDC checkout on Solana or Base.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bundled signing flows can expose wallet private keys and submit irreversible blockchain payments.

Mitigation: Avoid private-key CLI signing with valuable wallets; prefer browser or hardware wallet signing and verify recipient, token, amount, and fees before approving.

Risk: Order creation sends buyer email, shipping details, wallet address, and purchase information to api.purch.xyz.

Mitigation: Use only data appropriate for the Purch API service and review the transaction and checkout details before submitting an order.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/purch-agent/skills/agentic-commerce)
- [Purch API base URL](https://api.purch.xyz)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline JSON, Bash, Python, and TypeScript examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include API request examples, checkout parameters, transaction-signing commands, and fallback browser-checkout guidance.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
