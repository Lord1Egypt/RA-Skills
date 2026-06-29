## Description: <br>
Extracts structured identity data from passports, driver's licenses, and national ID cards for KYC and onboarding, returning typed JSON with confidence flags and redaction support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[uday390](https://clawhub.ai/user/uday390) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and operations teams use this skill to extract identity fields from uploaded ID documents for KYC, onboarding, account recovery, fraud operations, travel, and hospitality workflows. It is intended for authorized processing of identity documents with consent and appropriate compliance controls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Identity documents contain sensitive personal data and are sent to DeepRead's API for processing. <br>
Mitigation: Use the skill only for authorized KYC, onboarding, or verification workflows with consent, approved retention policies, and applicable compliance review. <br>
Risk: The DEEPREAD_API_KEY credential is required to call the service. <br>
Mitigation: Store the API key in a secret manager or environment variable, avoid committing it to source control, and rotate it if exposure is suspected. <br>
Risk: Low-quality scans, glare, or worn print can produce fields that need review. <br>
Mitigation: Route fields marked needs_review to manual verification before making identity, eligibility, or fraud decisions. <br>
Risk: Storing raw ID images can increase privacy and compliance exposure. <br>
Mitigation: Extract the minimum fields needed, redact images before storage or sharing, and avoid retaining full identity documents unless required. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/uday390/deepread-id-documents) <br>
- [DeepRead Homepage](https://www.deepread.tech) <br>
- [DeepRead Dashboard](https://www.deepread.tech/dashboard) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON examples, Python snippets, shell commands, and configuration instructions.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires DEEPREAD_API_KEY and sends identity document images to DeepRead's API for extraction and redaction workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
