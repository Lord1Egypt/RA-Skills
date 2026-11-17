## Description:

Free read-only market monitoring for Hyperliquid and LN Markets that lets agents check live prices, public balances, and positions without trade execution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nickymick8](https://clawhub.ai/user/nickymick8)

### License/Terms of Use:

MIT

## Use Case:

External users and agent developers use this skill to monitor crypto market prices and read Hyperliquid account balances or positions from a public wallet address. It is intended for read-only market intelligence, not trading execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact advertises a Telegram trading upgrade outside the skill's read-only monitoring scope.

Mitigation: Use the skill only for read-only price, balance, and position monitoring; do not send secrets, wallet approvals, or funds to the advertised bot unless that separate service is independently verified and audited.

Risk: Balance and position monitoring depends on a public Hyperliquid wallet address supplied through an environment variable.

Mitigation: Provide only public wallet addresses and keep private keys, seed phrases, API keys, and trading credentials out of the agent environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nickymick8/skills/claw-trader-lite)
- [Hyperliquid public API](https://api.hyperliquid.xyz)
- [LN Markets public API](https://api.lnmarkets.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces read-only monitoring guidance and Python API usage patterns; runtime calls may return market prices, balances, or position dictionaries.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
