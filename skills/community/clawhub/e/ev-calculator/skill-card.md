## Description:

Calculates expected value for trading or betting decisions, including basic EV, Polymarket edge, odds conversion, arbitrage boundary checks, and optional Kelly sizing guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jinboh68-prog](https://clawhub.ai/user/jinboh68-prog)

### License/Terms of Use:

MIT-0

## Use Case:

External users, analysts, and developers use this skill to calculate expected value from probability, win/loss, and market-price assumptions. It supports quick decision analysis for EV-positive or EV-negative scenarios, including Polymarket-style probability comparisons.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Calculator inputs may be sent to the declared remote API.

Mitigation: Review input sensitivity and submit only scenarios that are appropriate for the remote calculator.

Risk: Use may require a 0.01 USDC x402 payment.

Mitigation: Confirm the cost, chain, wallet, and payment policy before enabling payment-capable execution.

Risk: Expected-value output could be mistaken for financial advice or used directly in automated trading.

Mitigation: Treat results as decision support, independently validate assumptions, and account for fees, slippage, funding costs, and sample-size limits.

Risk: Mutable source references can change after review.

Mitigation: Prefer a pinned release or reviewed package before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jinboh68-prog/skills/ev-calculator)
- [Python](https://www.python.org/)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Markdown or JSON numeric EV calculations with brief verdicts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use a paid x402 remote API endpoint; local Python examples are also documented.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
