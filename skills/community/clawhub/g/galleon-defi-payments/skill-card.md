## Description:

Use when planning or reconciling stablecoin transfers, paid x402 requests, token streaming, vesting or airdrop distribution. Match the payment obligation to official wallet and protocol tools; distinguish authorization, settlement and service delivery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[galleonlabs](https://clawhub.ai/user/galleonlabs)

### License/Terms of Use:

MIT

## Use Case:

Developers and payment operators use this skill to plan and reconcile token transfers, paid HTTP requests, vesting, and token streams. It helps them check payment terms, permissions, settlement, and service delivery before reporting an outcome.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security review confidence is medium because one referenced path could not be resolved.

Mitigation: Review the missing reference and the related payment guidance before enabling wallet actions.

Risk: A payment request or stream can commit funds under terms that differ from the user's intent.

Mitigation: Confirm the recipient, asset, network, amount, fees, duration, and enforceable limits before signing; use only existing explicit authorization.

Risk: A timeout can leave settlement uncertain and a retry can duplicate payment.

Mitigation: Reconcile the original payment identifier, transaction, nonce, and receipt before retrying.

## Reference(s):

- [Provider access and payment models](references/providers.md)
- [Payment workflows and evaluation cases](references/workflows.md)
- [x402 v2 verification and recovery](references/x402-v2.md)
- [Worked stream calculation](references/task-examples.md)
- [x402 HTTP contract](https://docs.x402.org/core-concepts/http-402)
- [x402 payment identifier extension](https://docs.x402.org/extensions/payment-identifier)
- [Coinbase x402 buyer guide](https://docs.cdp.coinbase.com/x402/buyer/quickstart)
- [Sablier agent guides](https://docs.sablier.com/guides/ai-agents)
- [Sablier Flow overview](https://docs.sablier.com/concepts/flow/overview)
- [Superfluid agent skills](https://github.com/superfluid-org/skills)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Analysis]

**Output Format:** [Markdown plans, checks, calculations, and payment or stream receipt summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Describes bounded payment terms and observed status; the skill grants no spending authority.]

## Skill Version(s):

0.3.0 (source: frontmatter and server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
