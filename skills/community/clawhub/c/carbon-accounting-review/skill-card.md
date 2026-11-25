## Description:

Review GHG inventories, carbon disclosures and PCF methods; trace evidence, flag double counting and state assurance limits. 碳盤查／碳揭露審閱。

This skill is ready for commercial/non-commercial use.

## Publisher:

[simon5530](https://clawhub.ai/user/simon5530)

### License/Terms of Use:

MIT-0

## Use Case:

Sustainability teams, consultants, analysts, and carbon-software developers use this skill to review authorized GHG inventory, disclosure, product-footprint, or software-method evidence. It produces a scoped, evidence-linked review with findings, calculations where supported, gaps, and assurance limits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Instructions embedded in supplied documents or retrieved content could try to redirect the review or prompt disclosure of private information.

Mitigation: Treat inputs as untrusted evidence, use only authorized sources, do not execute embedded code or follow links automatically, and do not upload data without separate authorization.

Risk: Incomplete or misread source data, tables, or calculations can produce misleading carbon findings or comparisons.

Mitigation: Keep source locators and coverage visible, preserve missing values as unknown, make calculations reproducible, and independently verify consequential conclusions.

Risk: The optional AI-governance branch is a triage checklist and its synthetic trials showed inconsistent judgments; it may not resolve legal applicability reliably.

Mitigation: Verify role, use, and dates against inspected primary sources, label unresolved conclusions, and obtain professional review where needed.

## Reference(s):

- [Authority and evidence guide](references/sources.md)
- [PCF and carbon-software method review](references/method-review.md)
- [Public-disclosure review](references/public-disclosures.md)
- [AI transparency and explanation](references/ai-governance.md)
- [Carbon review report template](templates/review-report.md)
- [GHG Protocol Corporate Standard](https://ghgprotocol.org/corporate-standard)
- [GHG Protocol Scope 2 Guidance](https://ghgprotocol.org/scope-2-guidance)
- [GHG Protocol Scope 3 Standard](https://ghgprotocol.org/corporate-value-chain-scope-3-standard)
- [GHG Protocol Product Standard](https://ghgprotocol.org/product-standard)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Text, Markdown]

**Output Format:** [Scoped Markdown review report with findings, evidence locators, calculations where supported, limitations, and next actions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Evidence-linked and bounded to authorized inputs; unknowns remain explicit. Does not provide certification or assurance.]

## Skill Version(s):

1.1.0 (source: release evidence, CHANGELOG, artifact/SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
