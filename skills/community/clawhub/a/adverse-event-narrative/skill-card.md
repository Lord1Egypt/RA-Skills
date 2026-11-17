## Description:

Generate CIOMS-compliant adverse event narratives for Individual Case Safety Reports (ICSR), creating structured pharmacovigilance documents that follow CIOMS I and ICH E2B standards from case data for regulatory submission to health authorities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Drug safety, pharmacovigilance, clinical operations, and regulatory teams use this skill to draft standardized adverse event narratives from structured case data for ICSR workflows. Outputs are drafts for qualified medical and safety review before regulatory submission.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Draft narratives may be incomplete, medically inaccurate, or unsuitable for direct regulatory submission.

Mitigation: Keep generated narratives under qualified drug-safety or physician review, and verify causality, MedDRA terminology, dates, outcomes, and required ICSR fields before use.

Risk: Case data can contain patient identifiers or sensitive health information.

Mitigation: Use de-identified case data and review outputs for privacy-sensitive details before sharing or submitting them.

Risk: English-focused examples and terminology may not satisfy every regional or language-specific reporting workflow.

Mitigation: Apply local regulatory, translation, and medical review processes for non-English or region-specific submissions.

## Reference(s):

- [CIOMS I Guidelines](references/CIOMS_I_Guidelines.md)
- [ICSR Narrative Template](references/ICSR_Template.md)
- [MedDRA Coding Reference](references/MedDRA_Reference.md)
- [Quick Reference Guide](references/Quick_Reference.md)
- [Sample Case 001](references/sample_case_001.json)
- [Minimal Sample Case](references/sample_case_minimal.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with inline shell commands and generated plain-text adverse event narratives.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated narratives are drafts and require qualified drug-safety or physician review before regulatory submission.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
