## Description:

Bridge Cost Optimizer helps agents compare cross-chain bridge routes by estimated USD fee, ETA, hops, and cheapest, fastest, or balanced preference.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ssidharhubble](https://clawhub.ai/user/ssidharhubble)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agents use this skill to compare cross-chain token bridge route estimates and choose a cheapest, fastest, or balanced option before independently verifying with a bridge provider.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recommendations may be misleading because several advertised live quotes are local estimates.

Mitigation: Treat results as informational and verify the selected route directly with the bridge provider before signing a transaction.

Risk: Estimates may rely on incorrect token decimals or Ethereum-only token addresses.

Mitigation: Confirm token addresses, decimals, amount, source chain, and destination chain in the bridge provider interface before use.

Risk: Public quote endpoints can fail, rate-limit, or return stale values while rates move.

Mitigation: Refresh quotes close to execution time and avoid acting on recommendations if provider calls fail or return inconsistent data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ssidharhubble/skills/bridge-cost-optimizer)
- [Across suggested-fees API](https://app.across.to/api/suggested-fees)
- [CoinGecko simple price API](https://api.coingecko.com/api/v3/simple/price)
- [deBridge DLN create transaction API](https://dln.debridge.finance/v1.0/dln/order/create-tx)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text CLI summaries and tables, with agent-facing Markdown command examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Does not sign or send transactions; route values should be verified with bridge providers before use.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
