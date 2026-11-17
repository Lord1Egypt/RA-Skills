## Description:

Guides agents through non-custodial cross-chain route quotes and caller-approved unsigned wallet actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[odaiin](https://clawhub.ai/user/odaiin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and wallet users can evaluate supported bridge routes and prepare caller-approved unsigned actions for cross-chain transfers or agent-wallet funding. They independently check the quote and sign and submit actions in their own wallet.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A stale or misleading quote or route may lead to incorrect fees, amounts, or recipients.

Mitigation: Verify the fresh fee-inclusive quote, chain, amount bounds, recipient, and action details before signing.

Risk: Wallet credentials or session tokens may be exposed during action preparation.

Mitigation: Never share private keys or seed phrases; protect session tokens and sign and submit only in your own wallet.

Risk: Cross-chain transfers are sequential and non-atomic.

Mitigation: Confirm workflow state and actual asset location before progressing or retrying an action.

## Reference(s):

- [AssetFare Route on ClawHub](https://clawhub.ai/odaiin/skills/assetfare-route)
- [AssetFare v2 OpenAPI specification](https://api.assetfare.dev/v2/openapi.json)
- [AssetFare route economics](https://assetfare.dev/route-economics.json)

## Skill Output:

**Output Type(s):** [Guidance, Text]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Fresh quote summaries and guidance for unsigned action handoff; no signing or submission.]

## Skill Version(s):

1.1.1 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
