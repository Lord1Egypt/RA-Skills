## Description:

Real-time OCR and data extraction API by Veryfi (https://veryfi.com). Extract structured data from receipts, invoices, bank statements, W-9s, purchase orders, bills of lading, and any other document. Use when you need to OCR documents, extract fields, parse receipts/invoices, bank statements, classify documents, detect fraud, or get raw OCR text from any document.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dbirulia](https://clawhub.ai/user/dbirulia)

### License/Terms of Use:

UNLICENSED

## Use Case:

Developers and AI-agent users use this skill to send authorized documents to Veryfi for OCR, structured field extraction, document classification, fraud signals, and raw text extraction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Documents are sent to Veryfi for processing, which creates privacy risk for sensitive or regulated files.

Mitigation: Process only documents you are authorized to send, test with non-sensitive samples first, and review Veryfi retention and compliance requirements before production use.

Risk: Veryfi credentials can be exposed if placed in code, logs, or shared configuration files.

Mitigation: Use environment variables or a secret store, avoid committing credentials, restrict local config permissions, rotate keys, and monitor usage.

Risk: Private URLs, presigned URLs, passports, tax forms, checks, bank statements, and medical-related documents may contain highly sensitive data.

Mitigation: Do not process those inputs unless authorization, retention expectations, and compliance obligations have been reviewed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dbirulia/skills/documents-ai)
- [Veryfi API Documentation](https://docs.veryfi.com/)
- [Veryfi](https://veryfi.com)
- [Veryfi API Credentials](https://app.veryfi.com/api/settings/keys/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with curl examples, configuration snippets, and JSON response schemas]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Veryfi credentials; API responses can include structured document data, fraud signals, confidence details, bounding boxes, URLs, and raw OCR text.]

## Skill Version(s):

1.0.1 (source: server release evidence; package.json reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
