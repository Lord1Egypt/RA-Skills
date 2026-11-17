## Description:

AI-powered smart contract security audit with x402 payment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luka1968](https://clawhub.ai/user/luka1968)

### License/Terms of Use:

MIT-0

## Use Case:

External smart-contract developers and auditors can request an AI-assisted audit of an EVM contract, check its audit status, and retrieve basic on-chain contract information.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill description claims a fixed 3 USDC/Base audit charge, while release security guidance says the pricing disclosures conflict with the service.

Mitigation: Before authorizing payment, verify the live quote, network, and recipient; do not rely on the fixed-price claim.

Risk: Payment may settle before the audit report succeeds.

Mitigation: Review payment and refund conditions before authorizing a paid audit.

Risk: Self-hosted deployments have reported concerns around public error disclosure, replay handling, settlement-based access, and data retention.

Mitigation: Address those deployment issues before accepting live payments, and avoid exposing secrets in public errors.

Risk: An AI-assisted report can be mistaken for confirmation that a contract is safe.

Mitigation: Treat findings as preliminary screening and independently verify them; absence of findings is not proof of safety.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/luka1968/skills/agentsafe)
- [Source repository (server-resolved provenance)](https://github.com/luka1968/agentsafe)
- [Agentsafe MCP endpoint](https://x402.workfern.com/mcp)

## Skill Output:

**Output Type(s):** [Security findings, Contract metadata, Audit task status, JSON]

**Output Format:** [Structured JSON tool responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Audit reports are preliminary screening, not a guarantee of contract safety.]

## Skill Version(s):

0.1.0 (source: pyproject.toml, ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
