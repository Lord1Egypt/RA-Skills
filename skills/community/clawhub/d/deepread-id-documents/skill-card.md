## Description:

Extract structured data from passports, driver's licenses, and national ID cards for KYC/onboarding as typed JSON with per-field review flags and optional PII redaction guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[uday390](https://clawhub.ai/user/uday390)

### License/Terms of Use:

MIT-0

## Use Case:

External teams and developers use this skill to extract identity-document fields for KYC, onboarding, age or expiry checks, account recovery, fraud operations, and travel or hospitality check-in workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Identity documents are sent to DeepRead's API for extraction.

Mitigation: Install and use only when authorized to process the documents, with appropriate consent, and review DeepRead's privacy terms before sending files.

Risk: Low-confidence or glare-affected fields may be incorrect.

Mitigation: Route fields marked needs_review to manual verification before accepting or storing the extracted data.

## Reference(s):

- [DeepRead homepage](https://www.deepread.tech)
- [DeepRead dashboard](https://www.deepread.tech/dashboard)
- [DeepRead ID Documents on ClawHub](https://clawhub.ai/uday390/skills/deepread-id-documents)

## Skill Output:

**Output Type(s):** [JSON, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with JSON, Python, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires DEEPREAD_API_KEY; extraction results include per-field needs_review flags.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
