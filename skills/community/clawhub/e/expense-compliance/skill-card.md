## Description:

Reviews receipts against a user's expense policy, checks for duplicates, and provides evidence-backed compliance recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[youteacher](https://clawhub.ai/user/youteacher)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and expense reviewers use this skill to extract receipt details, compare claims with a versioned reimbursement policy, flag duplicates or uncertain results for human review, and export an evidence-backed audit report. Its findings are advice, not payment approval or official invoice verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Receipt images, OCR text, policy data, and claim details are sent to the AI Skills platform.

Mitigation: Confirm that the user accepts this data transfer before installation or use; avoid exposing complete receipt or tax identifiers in logs and reports.

Risk: A general platform API key may have broader access than a product-specific key.

Mitigation: Prefer EXPENSE_COMPLIANCE_API_KEY for tighter credential scope and never place complete API keys in chat logs or exported reports.

Risk: Low-confidence OCR or possible duplicates can lead to misleading compliance conclusions.

Mitigation: Require explicit user verification of uncertain receipt fields, route possible duplicates for human review, and do not treat compliance findings as payment approval or official invoice validation.

## Reference(s):

- [Expense Compliance on ClawHub](https://clawhub.ai/youteacher/skills/expense-compliance)
- [AI Skills platform](https://ai-skills.open-idea.net)
- [API key configuration](https://ai-skills.open-idea.net/skill-docs/expense-compliance/API-KEY.md)
- [HTTP requests, idempotency, and polling](https://ai-skills.open-idea.net/skill-docs/expense-compliance/HTTP-REQUESTS.md)
- [Operations, rules, and results](https://ai-skills.open-idea.net/skill-docs/expense-compliance/OPERATIONS.md)
- [Evidence, security, and human review](https://ai-skills.open-idea.net/skill-docs/expense-compliance/BEHAVIOR-RULES.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, JSON]

**Output Format:** [Text guidance and private Markdown or JSON audit reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports retain the audited policy version, findings, and supporting evidence; findings do not authorize payment.]

## Skill Version(s):

1.2.0 (source: server-resolved release metadata and skill packageVersion)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
