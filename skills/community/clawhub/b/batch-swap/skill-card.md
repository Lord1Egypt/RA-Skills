## Description:

Executes multiple token swaps in sequence for rebalancing or multi-step trading plans, with independent safety validation for each swap.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wpank](https://clawhub.ai/user/wpank)

### License/Terms of Use:


## Use Case:

Developers and trading agents use this skill to parse, validate, execute, and summarize batches of Uniswap token swaps for portfolio rebalancing or multi-step trading workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can trigger multiple real token trades in one workflow.

Mitigation: Require explicit approval before execution and review every token, chain, amount, slippage, gas estimate, and batch total.

Risk: Installation instructions reference mutable remote installers.

Mitigation: Install only from a pinned, reviewed version or commit.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wpank/skills/batch-swap)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with transaction summaries and error guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include swap-by-swap status, transaction hashes, gas totals, partial-failure details, and suggested corrective actions.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
