## Description:

Helps prepare and review common mainland China business tax calculations, supporting workpapers, and filing checklists.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kaimomo99](https://clawhub.ai/user/kaimomo99)

### License/Terms of Use:

MIT-0

## Use Case:

Business tax and payroll staff in mainland China use this skill to reconcile records, calculate common VAT, surcharges, corporate and individual income taxes, and stamp duty, and prepare draft filing workpapers for review.

### Deployment Geography for Use:

Mainland China

## Known Risks and Mitigations:

Risk: Outdated or inapplicable tax rules can produce incorrect filing figures.

Mitigation: Verify current national and local policy, tax period, and eligibility before relying on draft calculations or filing.

Risk: Business and payroll records may contain sensitive personal and financial information.

Mitigation: Limit access to required records, keep customer inputs outside the public skill repository, and omit credentials and unnecessary identifiers from reports.

Risk: Draft calculations or an attempted filing may be mistaken for an accepted return or completed payment.

Mitigation: Obtain explicit approval for each official submission, correction, refund, or payment, and confirm acceptance and payment separately against official receipts.

## Reference(s):

- [ClawHub release](https://clawhub.ai/kaimomo99/skills/china-tax-clerk)
- [Project homepage (declared; import provenance unavailable)](https://github.com/KAImomo99/china-tax-clerk)
- [Calculation interface and limits](references/calculator.md)
- [Tax policy index](references/policies.md)
- [Filing review workflow](references/workflow.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Guidance]

**Output Format:** [Draft workpapers and checklists in Markdown; local tax calculations in JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Calculation outputs are drafts, not proof of filing or payment; the built-in policy snapshot is dated 2026-10-10 and the calculator accepts 2026–2027 tax periods.]

## Skill Version(s):

0.1.0 (source: ClawHub release and SKILL.md metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
