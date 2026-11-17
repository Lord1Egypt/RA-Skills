## Description:

Helps agents set up and diagnose DeFi RPC access, managed wallets, payment permissions, and Hermes tool connections before protocol-specific work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[galleonlabs](https://clawhub.ai/user/galleonlabs)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to check DeFi agent infrastructure, diagnose connection failures, and establish the minimum read-only access needed for a requested task without treating readiness as transaction authorization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Provider login, wallet sessions, or payment setup could expand financial authority beyond the requested task.

Mitigation: Review each authorization and enforce provider-level scopes and spending limits; connection checks alone do not approve trades, transfers, signatures, or paid API calls.

Risk: A successful connection test could be mistaken for authenticated access or transaction readiness.

Mitigation: Verify the selected chain, freshness, account, and permissions with a bounded read; report unverified capabilities as unknown.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/galleonlabs/skills/galleon-defi-infra)
- [Readiness diagnostics](references/readiness.md)
- [RPC and Alchemy](references/rpc-alchemy.md)
- [Managed wallets](references/wallets.md)
- [Payments and authority](references/payments.md)
- [Hermes wiring](references/hermes.md)
- [CLI recovery](references/cli-recovery.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions, Readiness reports]

**Output Format:** [Markdown guidance and optional JSON diagnostics]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports observed chain, freshness, access scope, and remaining limitations; does not authorize transactions.]

## Skill Version(s):

0.4.1 (source: skill frontmatter and ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
