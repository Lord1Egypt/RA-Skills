## Description:

Provides a Python client for the 1inch API v5.2 to request DEX quotes, token data, approval transaction data, and swap transaction payloads across multiple chains.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eric1099281](https://clawhub.ai/user/eric1099281)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to integrate 1inch DEX quote and swap-data workflows into blockchain tooling. It is suitable for preparing transaction data that must be independently verified before wallet signing or broadcast.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill prepares financial transaction data and the security evidence flags mishandled chain selection and token approval checks.

Mitigation: Before signing, independently verify the chain, router contract, token addresses, amount, spender, slippage, and calldata in a wallet or separate verification layer.

Risk: Using the skill sends a 1inch API key, wallet address, token selections, and trade amounts to 1inch.

Mitigation: Use an API key with appropriate limits and avoid sending sensitive wallet or trading information unless this disclosure is acceptable for the deployment.

## Reference(s):

- [ClawHub 1inch Skill Page](https://clawhub.ai/eric1099281/skills/1inch)
- [1inch Developer Portal](https://portal.1inch.dev/)
- [1inch Swap API v5.2 Base URL](https://api.1inch.dev/swap/v5.2)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown guidance with Python code examples and JSON-like API response structures]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces transaction data and API integration guidance; it does not itself complete wallet signing or blockchain broadcast.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
