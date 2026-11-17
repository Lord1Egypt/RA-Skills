## Description:

Analyzes Uniswap Firepit burn economics by producing governance-grade reports on historical burn P&L, fee accumulation trends, fee source breakdowns, competitive dynamics, and profitability projections.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wpank](https://clawhub.ai/user/wpank)

### License/Terms of Use:


## Use Case:

UNI holders, governance participants, and protocol researchers use this skill to analyze historical Firepit burn profitability, protocol fee accumulation, fee composition, and future burn scenarios. It is intended for analytical reporting only and does not execute burns or provide real-time monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation examples use mutable npx/latest commands that may resolve different code in the future.

Mitigation: Install only from a trusted artifact and prefer an immutable, pinned ClawHub release or exact Git commit.

Risk: Historical P&L and fee source analysis may be approximate when price history, burn depth, accumulation data, or token pricing is sparse.

Mitigation: Review reported data availability and treat projections as scenario analysis rather than execution guidance.

Risk: The skill's analysis could be mistaken for an instruction to execute a burn or make governance decisions automatically.

Mitigation: Use the output as research support only; review conclusions before governance use and do not use this skill for transaction execution.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wpank/skills/analyze-burn-economics)
- [SKILL.md](artifact/SKILL.md)
- [README.md](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown analytical report with tables, summary metrics, and projections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only analytical output based on Uniswap burn history, fee accumulation, Firepit state, TokenJar balances, and UNI price data.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
