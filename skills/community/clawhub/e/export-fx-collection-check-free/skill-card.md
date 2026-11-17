## Description:

A local Chinese-language checker that reconciles export declaration and foreign-exchange collection tables by recalculating row formulas, totals, duplicates, blanks, and negative amounts with cited source lines.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Finance, cashier, and export operations teams use this skill during monthly closing, reconciliation, and review to check whether export declaration amounts, commission-adjusted receivables, collected FX, and write-off differences agree. It provides deterministic table checks and identifies missing evidence instead of giving tax, legal, or foreign-exchange compliance advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Input tables may contain sensitive export declaration and foreign-exchange collection data.

Mitigation: Run only when a local Chinese-language reconciliation checker is needed, provide only the intended input file, and avoid sharing results beyond the review workflow.

Risk: Arithmetic reconciliation findings could be mistaken for tax, legal, or foreign-exchange compliance advice.

Mitigation: Treat results as table checks only and confirm compliance decisions against contracts, bank records, tax requirements, and foreign-exchange rules.

Risk: The free release intentionally omits several checks available outside this package.

Mitigation: Review the reported checks not run before relying on a clean result, especially for threshold, exchange-rate, over-collection, zero-declaration, or commission-rate questions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/export-fx-collection-check-free)
- [ClawHub publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Markdown guidance with shell commands and optional JSON checker output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs local read-only checks against user-provided table text or JSON; findings cite source lines and list checks not run.]

## Skill Version(s):

1.0.53 (source: server release metadata and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
