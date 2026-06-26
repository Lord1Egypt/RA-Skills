## Description: <br>
Redacts PII from PDFs, scanned images, and text files before sharing or sending to LLMs, using context-aware AI to detect 14 PII types and apply irreversible black-bar redaction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[uday390](https://clawhub.ai/user/uday390) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to redact personal information from PDFs, images, and text before sharing documents, sending content to LLMs, or preparing compliance, legal, medical, financial, HR, insurance, or training-data workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Original unredacted documents are sent to DeepRead's hosted service for processing. <br>
Mitigation: Use the skill only for documents you are permitted to send to DeepRead, and review DeepRead's privacy, retention, and compliance terms before processing regulated data. <br>
Risk: The DeepRead API key can authorize document processing if exposed. <br>
Mitigation: Store DEEPREAD_API_KEY outside shared configs, use a dedicated key when possible, and rotate the key if it may have been disclosed. <br>
Risk: Webhook delivery may expose results if sent to an uncontrolled endpoint. <br>
Mitigation: Use HTTPS webhook URLs you control and authenticate the receiving endpoint before relying on webhook-based processing. <br>


## Reference(s): <br>
- [DeepRead Homepage](https://www.deepread.tech) <br>
- [DeepRead PII Redaction API](https://api.deepread.tech/v1/pii/redact) <br>
- [DeepRead Privacy Policy](https://www.deepread.tech/privacy) <br>
- [DeepRead Dashboard](https://www.deepread.tech/dashboard) <br>
- [DeepRead Service Issues](https://github.com/deepread-tech/deep-read-service/issues) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, configuration, text] <br>
**Output Format:** [Markdown with inline JSON, bash, Python, and JavaScript examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides agents to upload documents to DeepRead, poll or use webhooks, download redacted files, and inspect redaction reports.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
