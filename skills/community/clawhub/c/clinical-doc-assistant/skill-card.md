## Description:

Clinical Doc Assistant helps clinicians, practice managers, and healthcare developers draft clinical documentation from FHIR R4 data or manual patient context, including SOAP notes, referrals, prior authorizations, discharge summaries, and care-plan narratives; it is not for diagnosis, prescribing, or unsupervised clinical judgment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[optimusprime19](https://clawhub.ai/user/optimusprime19)

### License/Terms of Use:

MIT-0

## Use Case:

Clinicians, practice managers, and healthcare developers use this skill to retrieve relevant FHIR R4 data or enter patient context manually, then produce reviewable documentation drafts for common clinical workflows. Generated text requires licensed clinician review before use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Patient data or PHI may be sent to external services when hosted generation is used.

Mitigation: Use synthetic sandbox data unless compliant infrastructure and BAAs are verified for every service that can receive PHI; minimize or redact patient data before LLM calls.

Risk: The hosted backend scaffold is not production-ready for healthcare use.

Mitigation: Before deployment, replace test-key authentication, persist credit accounting, restrict CORS, add rate limits, and complete compliance review.

Risk: Generated clinical documentation may be incomplete, inaccurate, or misleading if used without review.

Mitigation: Require licensed clinician review, editing, and signature before any generated draft is used in patient care or records.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/optimusprime19/skills/clinical-doc-assistant)
- [Publisher profile](https://clawhub.ai/user/optimusprime19)
- [Project homepage](https://github.com/optimusprime19/clinical-doc-assistant)
- [FHIR R4 Reference](FHIR-REFERENCE.md)
- [HAPI FHIR R4 sandbox](https://hapi.fhir.org/baseR4)
- [Epic FHIR developer portal](https://fhir.epic.com)
- [Cerner developer portal](https://code.cerner.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain text clinical documentation drafts with optional setup commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Drafts may include missing-data placeholders and must be reviewed, edited, and signed by a licensed clinician before use.]

## Skill Version(s):

1.0.4 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
