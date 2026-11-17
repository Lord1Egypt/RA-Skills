## Description:

Provides guidance for a locally tested agent wallet and payments app covering $PocketTag handles, payment requests, receipts, escrow, and reputation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eric-tijerina](https://clawhub.ai/user/eric-tijerina)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to understand and locally test the described wallet and payment flows. The documented service is not publicly deployed and should not be used for real payments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet, payment, and private-key claims have not been independently verified, and no public deployment is confirmed.

Mitigation: Do not use with real funds, private keys, card payments, or production wallets; inspect the server, contracts, and deployment and confirm the public URL before any real-world use.

Risk: Local demo funding and ledger records may be mistaken for settled payments.

Mitigation: Treat the local MVP as a test environment and confirm actual on-chain settlement separately.

## Reference(s):

- [AgentPocket ClawHub release](https://clawhub.ai/eric-tijerina/skills/agentpocket)
- [Homepage listed in skill metadata (not confirmed as a live service)](https://mini-tollbooth.onrender.com)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API request examples]

**Output Format:** [Markdown with inline commands and endpoint examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Describes local testing; no publicly deployed payment endpoint is confirmed.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
