## Description:

Integrate with the Alura Trading testnet API for EVM wallet authentication, trading sessions, market data, leaderboard, referrals, and USDC verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[evilboyajay](https://clawhub.ai/user/evilboyajay)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to understand and call Alura Trading testnet API routes for authentication, trade sessions, market data, referrals, leaderboard data, and USDC verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authenticated API routes include withdrawals, USDC transfers, position closes, close-all actions, reward claims, and cron-triggering calls that can affect funds or trading positions.

Mitigation: Require explicit user confirmation before any fund-transfer, position-closing, reward-claiming, or cron-triggering call, and use testnet credentials unless the target environment has been independently verified.

Risk: Bearer tokens and wallet signatures can authorize privileged account actions if exposed or reused.

Mitigation: Keep tokens and signatures scoped, short-lived, and out of logs or generated output whenever possible.

## Reference(s):

- [Alura testnet API documentation](https://testnet-api.alura.fun/api/docs)
- [Alura ClawHub skill page](https://clawhub.ai/evilboyajay/skills/alura)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with HTTP endpoint examples and JSON request bodies]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Authenticated routes require a Bearer token and should target the Alura testnet API base URL unless the user verifies another environment.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
