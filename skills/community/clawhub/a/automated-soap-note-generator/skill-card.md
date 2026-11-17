## Description:

Transforms unstructured clinical input, including dictation, transcripts, and rough notes, into standardized SOAP medical documentation drafts that require physician review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Clinicians, clinical documentation teams, and healthcare workflow builders use this skill to convert encounter text into a structured SOAP note draft for review before use in patient records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Clinical input may contain identifiable patient information.

Mitigation: Use only in a HIPAA-compliant environment for PHI and de-identify text when processing outside approved clinical systems.

Risk: SOAP drafts may contain incorrect facts, medications, dosages, negations, or clinical interpretation.

Mitigation: Require physician review and correction before entering any generated text into a patient record.

Risk: JSON output or shared folders can preserve raw transcripts or sensitive note content.

Mitigation: Avoid JSON output or shared storage when raw transcripts should not be persisted, and handle generated files under the organization's privacy policy.

Risk: The packaged requirements file includes unnecessary entries for the local script.

Mitigation: Review or remove unnecessary requirements before running dependency installation commands.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/aipoch-ai/skills/automated-soap-note-generator)
- [Clinical Documentation Guidelines](references/clinical_guidelines.md)
- [Medical Terminology Reference](references/medical_terminology.md)
- [Sample SOAP Notes](references/sample_soap_notes.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, guidance]

**Output Format:** [Structured SOAP note drafts in Markdown or JSON, with review guidance for clinical validation.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are documentation drafts only and must be reviewed for medical accuracy, medications, dosages, negations, and completeness before patient-record use.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
