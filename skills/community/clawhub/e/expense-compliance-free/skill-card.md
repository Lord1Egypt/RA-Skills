## Description:

A free local pre-check for reimbursement materials that compares one expense claim with invoices and reports duplicate invoice numbers, missing invoice fields, and unreplaced template placeholders with source line evidence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Finance employees and operations reviewers use this skill before reimbursement submission to identify duplicate invoice numbers, missing invoice number/date/seller/amount fields, and placeholder text in the supplied expense materials. It is a narrow precheck and does not decide whether an expense is reimbursable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reimbursement and invoice text can contain sensitive business or personal data.

Mitigation: Run the checker only in an approved local environment and avoid sharing input documents beyond the intended review process.

Risk: The output is a narrow precheck and can be mistaken for a full compliance, fraud, tax, or invoice-authenticity review.

Mitigation: Treat findings as triage evidence and require the normal finance, tax, and approval workflow before accepting or rejecting reimbursement.

Risk: No findings outside the free version's three checks may be misunderstood as full clearance.

Mitigation: Review the listed withheld checks and do not treat a clean result as coverage for omitted policy, arithmetic, date, tax, or authenticity checks.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/expense-compliance-free)
- [Publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [Human-readable text or structured JSON containing findings, severity, categories, line evidence, advice, executed checks, and withheld checks.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs on local Node.js inputs; insufficient material returns an insufficient_input result instead of a compliance conclusion.]

## Skill Version(s):

1.0.58 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
