## Description:

AI-powered Traditional Chinese Medicine prescription assistant for syndrome differentiation, classical formula recommendation, composition analysis, herb safety checking, dosage guidance, and formula modification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangfromchu-ai](https://clawhub.ai/user/wangfromchu-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and practitioners can use this skill as educational or clinician-supervised reference material for TCM intake, syndrome differentiation, formula comparison, prescription-style recommendations, and safety review. It should not be used for self-diagnosis, self-prescribing, emergency care, pregnancy care, pediatric care, or medication-interaction decisions without qualified clinical review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can produce individualized TCM diagnoses, prescriptions, and dosages that may be incorrect or unsafe.

Mitigation: Use outputs only as educational or clinician-supervised reference material and require review by a licensed TCM practitioner before any clinical use.

Risk: Pregnancy, pediatric cases, emergency symptoms, toxic herbs, and medication interactions carry elevated safety risk.

Mitigation: Do not rely on the skill for these decisions; escalate to qualified medical care and apply the artifact's mandatory safety-review workflow before considering any formula.

Risk: Users may share sensitive health details during the clinical workflow.

Mitigation: Minimize unnecessary personal data, avoid identifiers where possible, and handle health information according to applicable privacy requirements.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangfromchu-ai/skills/aky-tcm-prescription)
- [TCM Constitution Types & Clinical References](artifact/references/constitution-clinical.md)
- [TCM Diagnosis Guide](artifact/references/diagnosis-guide.md)
- [Aky TCM Prescription - Formula Analysis & Pattern Correspondence](artifact/references/formula-analysis.md)
- [TCM Formula Database](artifact/references/formula-database.md)
- [TCM Herb Reference](artifact/references/herb-reference.md)
- [TCM Safety Rules](artifact/references/safety-rules.md)
- [TCM Syndrome Differentiation Guide](artifact/references/syndrome-differentiation.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown with structured diagnostic, formula, dosage, modification, and safety-review sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include patient-intake summaries, TCM pattern analysis, formula tables, herb-role explanations, dosage ranges, cautions, and practitioner-review reminders.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
