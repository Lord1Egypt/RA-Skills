## Description: <br>
AI-powered shopping API for product search, shopping assistant responses, crypto order creation, and USDC checkout signing on Solana or Base. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[purch-agent](https://clawhub.ai/user/purch-agent) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent builders use this skill to search products, create orders, and integrate USDC checkout flows for Amazon and Shopify items on Solana or Base. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can ask for raw wallet private keys when using bundled signing scripts. <br>
Mitigation: Prefer browser checkout or a trusted wallet/hardware-wallet flow; use only a dedicated low-balance wallet for testing. <br>
Risk: Purchase and signing flows can send real irreversible USDC payments. <br>
Mitigation: Before signing, independently verify the merchant, USDC amount, chain, recipient or contract, and fees. <br>
Risk: Checkout requests send buyer email and shipping details to api.purch.xyz. <br>
Mitigation: Review what personal shipping data is sent and provide only information appropriate for the purchase. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/purch-agent/agentic-commerce) <br>
- [Purch API](https://api.purch.xyz) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown documentation with JSON examples, API calls, and Python or TypeScript command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the external Purch API and bundled Python/TypeScript scripts; purchase and signing flows can submit real blockchain transactions.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
