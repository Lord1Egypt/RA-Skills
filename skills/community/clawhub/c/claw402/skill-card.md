## Description:

Provides paid access to market data and AI API endpoints through x402 micropayments using USDC on Base.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tinkle-community](https://clawhub.ai/user/tinkle-community)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to query cryptocurrency, equity, forex, global time-series, and AI inference endpoints through a wallet-funded pay-per-call workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles a wallet private key and can initiate paid USDC API calls.

Mitigation: Install it only with a dedicated low-balance Base wallet, not a primary wallet.

Risk: Automatic chained use could spend funds without a clear budget.

Mitigation: Treat each invocation as potentially spending USDC and avoid automatic chained calls unless a budget is set.

Risk: The security summary flags weak guardrails and an unpinned payment SDK.

Mitigation: Verify the claw402 SDK version and gateway destination before use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/tinkle-community/skills/claw402)
- [Publisher Profile](https://clawhub.ai/user/tinkle-community)
- [claw402 Homepage](https://claw402.ai)
- [claw402 API Catalog](https://claw402.ai/api/v1/catalog)

## Skill Output:

**Output Type(s):** [Shell commands, API calls, JSON, Markdown, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires WALLET_PRIVATE_KEY and may spend USDC per invocation.]

## Skill Version(s):

1.3.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
