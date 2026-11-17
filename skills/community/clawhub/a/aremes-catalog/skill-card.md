## Description:

Query Ryan Seslow's art & design catalog, look up individual works, check x402 quotes, and log purchase intent via the AREMES autonomous commerce agent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ryanseslow](https://clawhub.ai/user/ryanseslow)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent developers use this skill to browse Ryan Seslow's catalog, inspect works, request current x402 licensing quotes, and create purchase intent records for Stripe or on-chain USDC checkout workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Checkout workflows may send buyer email, optional name or organization, transaction hash, and message text to Ryan Seslow/AREMES endpoints.

Mitigation: Use the skill only for intentional catalog and purchase workflows, and avoid entering unrelated sensitive information in optional message or buyer detail fields.

Risk: Payment or quote details may become outdated or may not match the buyer's intended transaction.

Mitigation: Confirm current quotes, wallet addresses, payment URLs, and order details independently before paying or submitting verification data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ryanseslow/skills/aremes-catalog)
- [Ryan Seslow catalog](https://ryanseslow.com/catalog.json)
- [AREMES agent metadata](https://aremes-enterprises.com/agent.json)
- [AREMES on-chain identity](https://agentfolio.bot/@aremes)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [Markdown guidance with HTTP examples and JSON request or response shapes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include catalog entries, quote details, payment verification results, checkout URLs, and workflow guidance.]

## Skill Version(s):

1.1.0 (source: frontmatter; server release metadata target version 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
