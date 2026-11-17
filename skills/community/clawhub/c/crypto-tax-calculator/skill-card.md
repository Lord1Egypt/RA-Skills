## Description:

Calculates FIFO crypto capital gains and losses from CSV buy/sell transactions, with short-term and long-term summaries and an optional Form 8949-style lot-by-lot CSV export.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ssidharhubble](https://clawhub.ai/user/ssidharhubble)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to estimate realized crypto gains and losses from exchange or wallet CSV exports, reconcile short-term and long-term exposure, and prepare lot-level reports for tax filing review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Tax filing decisions could be incorrect if FIFO estimates are treated as professional tax advice.

Mitigation: Treat outputs as filing preparation only and verify tax treatment with a licensed professional before filing.

Risk: Incomplete buy history can cause sells with missing cost basis to be skipped or misrepresented.

Mitigation: Use complete transaction history for every tracked asset and review missing-cost-basis warnings before relying on totals.

Risk: The tool does not handle wash-sale rules, staking or airdrop income basis, specific-lot identification, LIFO, or jurisdiction-specific tax rules.

Mitigation: Confirm that FIFO-only reporting is appropriate for the user's records and jurisdiction before using the report in tax preparation.

Risk: Transaction CSVs and generated reports can contain sensitive financial records.

Mitigation: Run the calculator locally only on CSVs intended for local processing and avoid sharing generated reports unnecessarily.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ssidharhubble/skills/crypto-tax-calculator)
- [README](artifact/README.md)
- [tax_calc.py](artifact/scripts/tax_calc.py)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Files, Guidance]

**Output Format:** [Markdown guidance with inline shell commands; console summaries and optional CSV file output from the bundled script.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write a lot-by-lot CSV report when an output path is supplied; console output includes per-asset and total gain/loss summaries.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
