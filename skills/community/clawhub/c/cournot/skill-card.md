## Description:

Query Cournot probabilities and divergence rankings; manage prepaid calls, balances, and API keys. Use only for /cournot or an explicit request to use Cournot, not for casual odds questions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cournot-ai](https://clawhub.ai/user/cournot-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users can ask an agent for Cournot event probability assessments and pricing-divergence rankings, or request account, API key, and prepaid call management. The skill returns the service's evidence and status in the user's language.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Event text is sent to Cournot, and queries can consume prepaid calls.

Mitigation: Send only event details the user intends to share and review applicable call costs before querying.

Risk: Payments can use real funds, and prepaid packs are non-refundable.

Mitigation: Before confirming, review the payment network, asset, amount, recipient, and approval requirement; treat mainnet payments as real-fund transactions.

Risk: Local API key files are plaintext, and wallet secrets are sensitive.

Mitigation: Protect the local credential files and never share wallet secrets in chat.

Risk: The optional wallet dependency is separate from this skill's security review.

Mitigation: Review the wallet dependency independently before installing it.

## Reference(s):

- [Cournot skill page](https://clawhub.ai/cournot-ai/skills/cournot)
- [Cournot documentation](https://skill.cournot.ai/)
- [Query flow](artifact/references/query-flow.md)
- [Divergence ranking](artifact/references/divergence-flow.md)
- [Account management](artifact/references/account.md)
- [Payment flow](artifact/references/payment.md)
- [Response format](artifact/references/response-format.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown tables for divergence rankings and concise text for queries and account actions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Divergence rankings are paginated, with up to 20 markets per page.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
