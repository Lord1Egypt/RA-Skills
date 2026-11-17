## Description:

A Chinese-language local Node.js checker that recomputes cargo-insurance ledger fields, flags duplicates, missing or negative values, and total-row mismatches, with findings tied to source line numbers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Logistics, freight forwarding, foreign trade, finance, and operations teams use this skill to check cargo-insurance and cargo-loss claim ledgers during monthly insurance reconciliation or after a cargo-loss claim. It helps recompute table-level arithmetic and consistency checks, while leaving insurance coverage, policy interpretation, and legal judgment outside its scope.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat arithmetic ledger checks as a complete insurance coverage or legal assessment.

Mitigation: Use the output only for table consistency review; have qualified reviewers assess policy coverage, claim eligibility, deductibles, rates, and legal questions.

Risk: The free version omits some checks, including underpayment, duplicate cargo coverage across policies, uninsured exposure, and ranked claim handling actions.

Mitigation: Review the reported checks_not_run or withheld-check list before relying on results, and perform separate review for omitted checks.

Risk: Incorrect headers, incomplete ledger text, or copied spreadsheet formatting can prevent reliable checking.

Mitigation: Provide a ledger with recognizable headers and required columns; when the skill reports insufficient input, correct the input instead of treating the absence of findings as clearance.

Risk: Cargo-insurance ledger data may contain commercially sensitive shipment and claim information.

Mitigation: Process only data suitable for local execution on the current machine and follow the organization's handling rules for shipment, policy, and claim records.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/cargo-insurance-claim-check-free)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Plain text or JSON results from a local command-line checker]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings cite source line numbers; insufficient input returns missing-field guidance instead of a conclusion.]

## Skill Version(s):

1.0.55 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
