## Description: <br>
Clinical Doc Assistant helps clinicians, practice managers, and healthcare developers draft clinical documentation from FHIR R4 patient data or manually supplied patient context. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[optimusprime19](https://clawhub.ai/user/optimusprime19) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Clinicians, practice managers, and healthcare developers use this skill to retrieve relevant FHIR R4 data and generate draft SOAP notes, referrals, prior authorization narratives, discharge summaries, care plans, and after-visit summaries. Outputs are documentation drafts for licensed clinical review, not diagnosis, prescribing, or independent clinical judgment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles patient data and can forward patient context to a hosted backend or model provider. <br>
Mitigation: Use sandbox or synthetic data for testing; before using real PHI, minimize or redact PHI and confirm HIPAA-eligible hosting plus BAAs with every service that receives PHI. <br>
Risk: The included backend scaffold is not safe to deploy unchanged for real patient data. <br>
Mitigation: Require real account-bound API keys, restrict CORS to approved origins, add rate limiting and audit controls, and complete production security review before deployment. <br>
Risk: Generated clinical documents may be incomplete, stale, or misleading if source data is missing or interpreted incorrectly. <br>
Mitigation: Treat all outputs as drafts that must be reviewed, edited, and signed by a licensed clinician; do not use the skill for diagnosis, prescribing, or independent clinical judgment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/optimusprime19/clinical-doc-assistant) <br>
- [Project Homepage](https://github.com/optimusprime19/clinical-doc-assistant) <br>
- [FHIR R4 Reference](artifact/FHIR-REFERENCE.md) <br>
- [HL7 FHIR ICD-10-CM System](http://hl7.org/fhir/sid/icd-10-cm) <br>
- [HAPI FHIR R4 Sandbox](https://hapi.fhir.org/baseR4) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and plain text clinical documentation drafts with optional shell commands, configuration snippets, FHIR query guidance, and backend code scaffolding] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Drafts may include missing-data placeholders and require licensed clinician review before use.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
