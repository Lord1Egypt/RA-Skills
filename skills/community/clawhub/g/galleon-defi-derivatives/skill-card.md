## Description:

Assesses DeFi perpetuals, options and funding-rate derivatives, prepares bounded exposure plans, and reconciles order and margin state.

This skill is ready for commercial/non-commercial use.

## Publisher:

[galleonlabs](https://clawhub.ai/user/galleonlabs)

### License/Terms of Use:

MIT

## Use Case:

Traders, analysts and developers use this skill to compare DeFi derivatives venues, plan hedges against a defined risk budget, and check orders, positions and margin before and after authorized actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Incorrect or stale market and account data can lead to losses or liquidation.

Mitigation: Use fresh official venue and account data, show observation times and downside scenarios, and avoid execution-ready claims when material data is missing.

Risk: A proposed trade, delegation, deposit, withdrawal or fee recipient could move or expose funds beyond the user's intent.

Mitigation: Keep each action within explicit user authorization; never share private keys or seed phrases, and review the exact terms in a trusted wallet or provider tool before approval.

Risk: An uncertain order outcome or competing account automation could result in duplicate or unintended exposure.

Mitigation: Reconcile existing orders, fills and active controllers before retrying or changing positions, and report unresolved state rather than assuming execution.

## Reference(s):

- [Galleon DeFi Derivatives on ClawHub](https://clawhub.ai/galleonlabs/skills/galleon-defi-derivatives)
- [Provider guidance](references/providers.md)
- [Exposure and order workflows](references/workflows.md)
- [Account and automation control](references/account-control.md)
- [GMX SDK overview](https://docs.gmx.io/docs/sdk/overview/)
- [Derive developer documentation](https://docs.derive.xyz/)
- [Boros official plugin](https://github.com/pendle-finance/pendle-ai/blob/main/packages/plugins/pendle-boros/README.md)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Markdown]

**Output Format:** [Markdown with exposure calculations, reviewable order plans and status summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes instrument and account scope, observation times, costs, downside constraints and unresolved gaps when available.]

## Skill Version(s):

0.1.5 (source: frontmatter and server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
