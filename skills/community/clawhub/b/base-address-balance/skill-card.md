## Description:

Looks up the latest ETH and token balances for one Base address, for $0.01 USDC per lookup from an existing agentcash or awal wallet.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scogib](https://clawhub.ai/user/scogib)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and wallet users can check the latest ETH and token balances of a Base address before a payment, transfer, or swap. Each lookup costs $0.01 USDC from an existing agentcash or awal wallet.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The lookup service receives the queried address and payment-related metadata.

Mitigation: Query only an address that is appropriate to share with the service.

Risk: Lookup charges can accumulate, and the conversation-wide budget depends on the agent tracking paid calls.

Mitigation: Approve a small, specific budget and use a wallet funded only for the intended spending.

Risk: First use downloads wallet packages whose internals were not audited; the awal fallback is untested.

Mitigation: Use the documented wallet choice and account for the untested awal fallback before relying on it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/scogib/skills/base-address-balance)
- [Service homepage](https://botx402.io)
- [Balance lookup endpoint](https://api.botx402.io/base-address-balance?via=clawhub)
- [agentcash package](https://www.npmjs.com/package/agentcash)
- [awal package](https://www.npmjs.com/package/awal)

## Skill Output:

**Output Type(s):** [JSON, Guidance]

**Output Format:** [JSON balance data with a concise textual explanation when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Latest-block, non-zero ETH and token balances; no labels, identities, or USD values. Additional pages require another $0.01 lookup.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
