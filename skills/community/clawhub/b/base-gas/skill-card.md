## Description:

Live and historical Base mainnet gas prices via x402, including cross-chain comparison and cheapest-hour scheduling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[memosr](https://clawhub.ai/user/memosr)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and on-chain agents use the skill to check Base gas costs, compare supported chains, review historical fee trends, and plan transaction timing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release evidence reports unpinned, changeable package installs.

Mitigation: Review the package and pin an approved version before installing or running it.

Risk: The release evidence reports transaction advice that may use unvalidated fees.

Mitigation: Check suggested fees against transaction limits and require the user's authorization before signing.

## Reference(s):

- [Base Gas on ClawHub](https://clawhub.ai/memosr/skills/base-gas)
- [Base Gas service](https://base-gas-x402.vercel.app)
- [Base Gas API health and history coverage](https://base-gas-x402-production.up.railway.app/health)

## Skill Output:

**Output Type(s):** [Analysis, API calls, Shell commands, Guidance, Transaction fee configuration]

**Output Format:** [JSON API results summarized as concise guidance, with shell commands when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Some history and comparison requests require USDC payment via x402; fee suggestions are informational and require fee-limit checks and authorized signing.]

## Skill Version(s):

1.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
