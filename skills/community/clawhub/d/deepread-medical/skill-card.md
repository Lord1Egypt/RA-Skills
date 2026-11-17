## Description:

DeepRead Medical Records helps agents extract structured data from medical records, lab reports, prescriptions, and clinical documents, and redact patient PII for healthcare document workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[uday390](https://clawhub.ai/user/uday390)

### License/Terms of Use:

MIT-0

## Use Case:

External users, healthcare developers, and operations teams use this skill to configure agents for structured extraction from clinical documents and PII redaction before sharing, archiving, or downstream LLM processing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may upload protected health information or other sensitive medical records to DeepRead and any configured BYOK model provider.

Mitigation: Use it only where those transfers are authorized and covered by required agreements, and test first with synthetic or already de-identified files.

Risk: External processing can conflict with retention, logging, data residency, or healthcare compliance requirements.

Mitigation: Review DeepRead and BYOK provider controls against organizational requirements before production use.

Risk: The sample workflow handles API keys and downloads processed documents.

Mitigation: Store credentials in environment variables and harden file handling, storage permissions, and error handling before production use.

## Reference(s):

- [DeepRead homepage](https://www.deepread.tech)
- [DeepRead Medical Records on ClawHub](https://clawhub.ai/uday390/skills/deepread-medical)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON schemas, Python and cURL examples, and API response JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires DEEPREAD_API_KEY and submits documents to DeepRead API endpoints.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
