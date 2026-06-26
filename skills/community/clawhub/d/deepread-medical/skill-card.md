## Description: <br>
DeepRead Medical Records helps agents extract structured data from medical records, lab reports, prescriptions, and clinical documents using prebuilt schemas and optional PII redaction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[uday390](https://clawhub.ai/user/uday390) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Healthcare operations teams, clinicians, and developers use this skill to turn medical documents into structured fields such as patient details, diagnoses, medications, vitals, and lab results, then review or redact patient information before downstream use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected medical documents are uploaded to DeepRead's external API. <br>
Mitigation: Use the skill only after confirming the vendor's legal and security posture for PHI, including a HIPAA BAA if needed. <br>
Risk: API key exposure could allow unauthorized use of the DeepRead account. <br>
Mitigation: Store the key only in the declared DEEPREAD_API_KEY environment variable and avoid hardcoding it in scripts or shared files. <br>
Risk: Redaction or extraction may mark uncertain fields for human review. <br>
Mitigation: Test redaction with synthetic data first and review any fields marked for human review before relying on the output. <br>


## Reference(s): <br>
- [DeepRead homepage](https://www.deepread.tech) <br>
- [ClawHub skill page](https://clawhub.ai/uday390/deepread-medical) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON schemas, Python examples, cURL commands, and operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes structured JSON extraction examples, polling workflow guidance, PII redaction guidance, and human-review flags for uncertain fields.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
