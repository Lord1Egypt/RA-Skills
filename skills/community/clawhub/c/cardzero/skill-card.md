## Description:

Openclaw helps agents use CardZero wallets to create and manage USDC payments, x402 paywalls, payment history, and A2A escrow jobs on Base within owner-defined limits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mrocker](https://clawhub.ai/user/mrocker)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use Openclaw to let an agent operate a CardZero USDC wallet for API payments, wallet checks, x402 purchases, and agent-to-agent escrow jobs, with human confirmation and owner-defined spending limits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives an agent authority to spend USDC from a configured wallet.

Mitigation: Use a low-balance wallet, strict per-transaction and daily limits, and require confirmation before sending payments.

Risk: API keys, claim keys, and configurable API endpoints can expose wallet access if mishandled.

Mitigation: Treat keys as secrets, use only the official CardZero API endpoint, and revoke or rotate credentials if they are exposed or sent to an untrusted API URL.

Risk: The artifact states the smart contract audit is still in progress.

Mitigation: Keep wallet balances low and follow the artifact's recommendation to limit balances to less than 100 USDC while audit status remains unresolved.

## Reference(s):

- [CardZero homepage](https://cardzero.ai)
- [ClawHub skill page](https://clawhub.ai/mrocker/skills/cardzero)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces wallet setup, payment, balance, transaction-history, x402, and A2A job instructions for an agent.]

## Skill Version(s):

1.4.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
