## Description:

Builds exact unsigned Hyperliquid trade tickets for selected actions with order details, sizing, and risk checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[galleonlabs](https://clawhub.ai/user/galleonlabs)

### License/Terms of Use:

MIT

## Use Case:

Traders and developers use this skill to prepare reviewable, unsigned Hyperliquid tickets for a chosen order or account action, including preflight checks and recovery plans. It does not sign or submit transactions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Account and subaccount addresses can reveal positions, orders, balances, and fees when used for planning.

Mitigation: Share only the public address needed for the requested plan and review the resulting account details before sharing them further.

Risk: Sharing signer secrets or private keys with the skill exposes wallet authority.

Mitigation: Never provide private keys or signer secrets; keep signing and submission outside this planning workflow.

Risk: An optional skill-install command is not version-pinned.

Mitigation: Review the package, version, and command before running any optional installation.

## Reference(s):

- [Hyperliquid Plan on ClawHub](https://clawhub.ai/galleonlabs/skills/galleon-hyperliquid-plan)
- [Ticket contract](artifact/references/ticket-contract.md)
- [Risk sizing](artifact/references/risk-sizing.md)
- [Hyperliquid Info endpoint](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/info-endpoint)

## Skill Output:

**Output Type(s):** [Markdown, Guidance]

**Output Format:** [Markdown unsigned trade ticket; optional JSON risk calculation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Identifies missing or stale preflight data; does not sign or submit actions.]

## Skill Version(s):

0.4.0 (source: ClawHub release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
