## Description: <br>
Extracts structured data from insurance claims, policies, EOBs, and loss reports, with schemas for claimant details, coverage, damages, adjuster notes, and PII redaction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[uday390](https://clawhub.ai/user/uday390) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Claims, policy, benefits, and loss-report teams use this skill to guide agents through extracting structured insurance document data and redacting claimant PII before sharing documents externally. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected insurance documents, claims, and EOBs may contain sensitive personal, health, financial, or claim data that is sent to DeepRead's external API. <br>
Mitigation: Use only documents approved for third-party processing, verify DeepRead privacy, retention, and compliance terms before production use, and redact PII before sharing processed files or outputs. <br>
Risk: The skill requires a DeepRead API key, which can expose account access if reused, hard-coded, or stored insecurely. <br>
Mitigation: Use a dedicated rotatable API key, provide it through DEEPREAD_API_KEY, and avoid committing credentials to files or prompts. <br>


## Reference(s): <br>
- [DeepRead homepage](https://www.deepread.tech) <br>
- [ClawHub skill page](https://clawhub.ai/uday390/deepread-insurance) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, API Calls, Configuration] <br>
**Output Format:** [Markdown with JSON, Python, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires DEEPREAD_API_KEY and sends selected documents to DeepRead's external API for processing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
