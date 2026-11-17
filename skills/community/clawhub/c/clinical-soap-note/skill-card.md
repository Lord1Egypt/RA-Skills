## Description:

Converts clinician or scribe raw encounter notes, dictation, or bullet points into a structured SOAP draft with gap flags and ICD-10/CPT coding prompts for mandatory clinician review before entry into the medical record.

This skill is ready for commercial/non-commercial use.

## Publisher:

[archlab-space](https://clawhub.ai/user/archlab-space)

### License/Terms of Use:

MIT-0

## Use Case:

Clinicians and medical scribes use this skill after patient encounters to structure raw notes, dictation, bullet fragments, or partial notes into a concise SOAP draft for clinician review and sign-off.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Patient information could be exposed if real identifiers are entered into systems that are not approved for PHI.

Mitigation: Use only in an approved patient-information environment and avoid sending real patient identifiers through unauthorized systems.

Risk: The SOAP draft could contain omissions or inaccurate restructuring if treated as final documentation.

Mitigation: Require a licensed clinician to verify, correct, and sign the draft before charting, billing, or clinical use.

Risk: Coding prompts could be mistaken for final ICD-10/CPT coding authority.

Mitigation: Treat coding content as non-binding prompts for coder or clinician review, not final codes.

## Reference(s):

- [Clinical Soap Note on ClawHub](https://clawhub.ai/archlab-space/skills/clinical-soap-note)
- [README](artifact/README.md)
- [CHANGELOG](artifact/CHANGELOG.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Structured Markdown SOAP note draft with flags, coding prompts, unresolved items, and clinician-review notice.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Draft output only; a licensed clinician must verify it before charting, billing, or clinical use.]

## Skill Version(s):

0.1.2 (source: server release metadata and CHANGELOG, released 2026-05-28)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
