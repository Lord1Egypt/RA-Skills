## Description:

Compares multiple documents for congruency and consistency, helping identify conflicting data points, missing fields, inconsistent terminology, and version mismatches.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dorjenorbulim](https://clawhub.ai/user/dorjenorbulim)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external reviewers, developers, and analysts use this skill to compare contracts, reports, forms, specifications, and other document sets for mismatches, missing fields, ambiguous values, and version inconsistencies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Confidential documents or report excerpts could be exposed if sent to unapproved external parsing, OCR, or sharing services.

Mitigation: Process documents locally when possible, redact sensitive content from shared reports, and use external parsing or OCR only with explicit approval.

Risk: Automated comparisons can misclassify ambiguous fields, OCR errors, or semantically equivalent wording as matches or conflicts.

Mitigation: Review discrepancy reports before relying on them, especially for legal, financial, identity, date, amount, and other critical fields.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dorjenorbulim/skills/document-congruence-checker)
- [Publisher profile](https://clawhub.ai/user/dorjenorbulim)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown discrepancy report with tables, congruence summary, criticality labels, and recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include extracted fields, document-by-document comparisons, congruence percentages, ambiguity notes, and prioritized action items.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
