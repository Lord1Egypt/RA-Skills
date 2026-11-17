## Description:

Discover supported cryptocurrencies, generate deposit addresses, and withdraw crypto to external wallets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[d9m1n1c](https://clawhub.ai/user/d9m1n1c)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to discover supported coins and networks, generate crypto deposit addresses, and perform quote-based withdrawals to external wallet addresses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crypto withdrawals can transfer funds to an unintended destination if the API endpoint, coin, network, address, amount, fees, or quote are wrong.

Mitigation: Before withdrawing, verify the API endpoint, coin, network, destination address, amount, fees, and quote.

Risk: Depositing on the wrong blockchain network can result in permanent loss of funds.

Mitigation: Confirm the selected blockchain network before generating or using a deposit address.

Risk: A transaction PIN authorizes withdrawal confirmation.

Mitigation: Ask for the transaction PIN only at confirmation time, never cache it, and use it only when the user intends to confirm the withdrawal.

## Reference(s):

- [Crypto Wallet ClawHub Skill Page](https://clawhub.ai/d9m1n1c/skills/aiotnetwork-crypto-wallet)
- [AIOT Payment API Base URL](https://payment-api-dev.aiotnetwork.io)

## Skill Output:

**Output Type(s):** [guidance, API calls, shell commands, configuration]

**Output Format:** [Markdown with endpoint references and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AIOT_API_BASE_URL for endpoint selection and authenticated wallet API access for protected operations.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
