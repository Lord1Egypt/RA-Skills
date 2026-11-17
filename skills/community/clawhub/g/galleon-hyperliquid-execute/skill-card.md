## Description:

Executes one explicitly approved Hyperliquid trading action through a trusted signer and reconciles the resulting exchange state.

This skill is ready for commercial/non-commercial use.

## Publisher:

[galleonlabs](https://clawhub.ai/user/galleonlabs)

### License/Terms of Use:

MIT

## Use Case:

Traders and their agents use this skill to execute an unchanged, reviewed Hyperliquid ticket after exact user approval, then verify orders, fills, and remaining exposure.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An unapproved or altered ticket could trigger a real financial action.

Mitigation: Require an unchanged reviewed ticket, exact user approval by ticket ID, and fresh pre-send checks before acting.

Risk: Signer secrets or untrusted tools could expose wallet authority.

Mitigation: Use a trusted signer or approved API wallet boundary; never enter private keys or seed phrases into the agent.

Risk: A delayed or unknown send result could lead to duplicate orders or unprotected exposure.

Mitigation: Send only once, reconcile exchange and account state, and stop rather than retry an uncertain action.

## Reference(s):

- [Hyperliquid Execution on ClawHub](https://clawhub.ai/galleonlabs/skills/galleon-hyperliquid-execute)
- [Hyperliquid API nonces and API wallets](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/nonces-and-api-wallets)
- [Hyperliquid Info endpoint](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/info-endpoint)
- [Hyperliquid Python SDK](https://github.com/hyperliquid-dex/hyperliquid-python-sdk)

## Skill Output:

**Output Type(s):** [Text, Markdown]

**Output Format:** [Markdown execution and reconciliation report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports order IDs, fills, fees, resulting exposure, protection, and unresolved uncertainty.]

## Skill Version(s):

0.4.0 (source: skill frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
