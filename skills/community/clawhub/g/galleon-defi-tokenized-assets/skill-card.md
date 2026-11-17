## Description:

Guides research into eligibility, custody, subscriptions, transfers, and redemption settlement for Ondo and OpenEden tokenized assets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[galleonlabs](https://clawhub.ai/user/galleonlabs)

### License/Terms of Use:

MIT

## Use Case:

Investors, analysts, and their agents use this skill to research product-specific access requirements and plan tokenized-asset subscriptions, transfers, and redemptions with documented settlement checks. It does not establish eligibility or authorize a transaction.

### Deployment Geography for Use:

Subject to issuer, product, investor, and jurisdictional restrictions; verify the applicable offering terms before acting.

## Known Risks and Mitigations:

Risk: Research or an indicative quote may be mistaken for authorization to place a binding order or move assets.

Mitigation: Require explicit, action-specific review before orders, approvals, signatures, transfers, purchases, or redemptions.

Risk: Eligibility, product terms, and market information can be unknown or stale.

Mitigation: Check current issuer sources and product-specific access requirements; label unknown eligibility and stop before restricted actions.

Risk: Credentials or identity documents may be exposed during onboarding or transaction preparation.

Mitigation: Keep credentials and identity documents out of chat and generated artifacts.

Risk: An accepted redemption or token burn may be mistaken for completed cash settlement.

Mitigation: Track requests, chain receipts, and actual proceeds independently; reconcile ambiguous outcomes before retrying.

## Reference(s):

- [Galleon DeFi Tokenized Assets on ClawHub](https://clawhub.ai/galleonlabs/skills/galleon-defi-tokenized-assets)
- [Provider reference notes](references/providers.md)
- [Eligibility and settlement workflow](references/workflows.md)
- [Ondo Finance API overview](https://docs.ondo.finance/api-reference/overview)
- [Ondo Finance OUSG redemption](https://docs.ondo.finance/qualified-access-products/ousg/redeeming)
- [OpenEden TBILL investor onboarding](https://docs.openeden.com/tbill/investor-onboarding)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Text]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Source-dated findings distinguish confirmed and unknown eligibility, transaction stages, and outstanding settlement evidence.]

## Skill Version(s):

0.1.3 (source: server release and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
