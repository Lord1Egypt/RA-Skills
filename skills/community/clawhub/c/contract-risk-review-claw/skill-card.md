## Description:

合同风险审查虾 supports Chinese-language and PRC-oriented contract review by identifying risky clauses, grading severity, and drafting revision suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tujinsama](https://clawhub.ai/user/tujinsama)

### License/Terms of Use:

MIT-0

## Use Case:

Legal, procurement, operations, and business users can use this skill to review contract text, uploaded contract files, or contract template comparisons for risky terms. It produces a structured review report with risk levels, clause locations, explanations, revision guidance, and replacement text.

### Deployment Geography for Use:

Global, for Chinese-language or PRC-oriented contract review support.

## Known Risks and Mitigations:

Risk: Contracts may contain sensitive or confidential information.

Mitigation: Process only contracts the user is authorized to review, and avoid sending unauthorized documents into the workflow.

Risk: Automated contract review can miss context-specific legal issues or produce guidance that is not sufficient for high-value agreements.

Mitigation: Have qualified counsel verify results for high-value, legally complex, or jurisdiction-sensitive agreements.

Risk: The embedded legal references and review posture are scoped to Chinese-language or PRC-oriented contract support.

Mitigation: Use the skill within that scope and seek jurisdiction-specific legal review for contracts governed by other legal systems.

## Reference(s):

- [风险条款库](references/risk-clauses.md)
- [合同模板库](references/contract-templates.md)
- [法律法规库](references/legal-regulations.md)
- [修订建议库](references/revision-suggestions.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown contract review report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include an overall grade, risk counts, severity-grouped clause findings, explanations, suggested edits, replacement text, and a review conclusion.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
