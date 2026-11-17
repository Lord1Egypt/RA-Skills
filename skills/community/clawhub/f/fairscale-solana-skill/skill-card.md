## Description:

Provides real-time Solana wallet reputation scores and risk assessments to inform and secure transaction decisions against fraudulent or risky actors.

This skill is ready for commercial/non-commercial use.

## Publisher:

[risheea](https://clawhub.ai/user/risheea)

### License/Terms of Use:


## Use Case:

Developers and agents working with Solana wallets use this skill to query FairScale reputation scores, transaction risk checks, and custom scoring workflows before transfers, airdrops, whitelists, lending decisions, or other wallet-gated actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet addresses, batch wallet lists, transaction amounts, and session tokens are sensitive financial metadata shared with FairScale.

Mitigation: Use the skill only when that external sharing is acceptable, minimize unnecessary wallet or amount disclosure, and protect session tokens.

Risk: Credit-backed endpoints depend on FairScale provider availability, pricing, and privacy terms.

Mitigation: Verify the provider, pricing, and privacy terms before prepaid-credit or production use.

## Reference(s):

- [FairScale Docs](https://docs.fairscale.xyz)
- [FairScale API Endpoint](https://x402.fairscale.xyz)
- [ClawHub Skill Page](https://clawhub.ai/risheea/skills/fairscale-solana-skill)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API Calls, Configuration instructions]

**Output Format:** [Markdown with inline bash, HTTP, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Describes FairScale wallet score, transaction risk, custom scoring, batch scoring, credits, and session token usage.]

## Skill Version(s):

0.1.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
