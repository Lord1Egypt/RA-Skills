## Description:

Runs an end-to-end Uniswap liquidity-provider workflow that scans opportunities, designs a strategy, assesses risk, prepares tokens, enters a position after user confirmations, and reports portfolio impact.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wpank](https://clawhub.ai/user/wpank)

### License/Terms of Use:


## Use Case:

External users and DeFi operators use this skill to delegate a full liquidity-provider workflow, from opportunity discovery through risk assessment, transaction confirmation, position entry, and portfolio reporting. It is intended for users who have capital ready and want an orchestrated Uniswap LP process rather than separate scan, strategy, trade, and reporting steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mutable install sources or package resolution could change the skill that is installed.

Mitigation: Install only from a trusted, pinned source when possible.

Risk: On-chain swaps and liquidity deposits can permanently move funds even when the workflow behaves as intended.

Mitigation: Confirm the chain, pool, token amounts, approvals, slippage, gas cost, and spending limits before approving any transaction.

Risk: The workflow handles live DeFi liquidity decisions where pool conditions, gas costs, and execution prices can change quickly.

Mitigation: Use the built-in confirmation gates and risk assessment output to review current terms before proceeding.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wpank/skills/full-lp-workflow)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown reports with structured status updates, recommendations, confirmation prompts, and portfolio summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires explicit user confirmation before token swaps and liquidity entry.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
