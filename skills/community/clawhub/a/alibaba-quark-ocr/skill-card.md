## Description:

This skill uses Quark Scan King's OCR service to extract text and structured fields from user-provided images, including screenshots, scanned documents, handwriting, tables, equations, IDs, invoices, medical reports, business licenses, and product images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yescan-ai](https://clawhub.ai/user/yescan-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill when an agent needs to turn a single static image, image URL, or base64 image into OCR text or document-specific structured data. It is intended for OCR and document information extraction, not image generation, video processing, live camera streams, or batch processing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Submitted images, including sensitive documents, are sent to Quark's OCR service using the configured API key.

Mitigation: Use this skill only when the user has approved the upload path; avoid or redact sensitive IDs, medical records, invoices, and other private documents unless the deployment is authorized for that data.

Risk: The security summary flags under-disclosed image-editing scenes and weak controls around third-party uploads and credentials.

Mitigation: Restrict permitted scene values to the documented OCR use cases unless an operator explicitly approves broader image-editing or document-conversion behavior.

Risk: The skill requires SCAN_WEBSERVICE_KEY for access to the third-party OCR service.

Mitigation: Provide the key through a managed environment secret, avoid exposing it in prompts or logs, and rotate it if it may have been shared.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yescan-ai/skills/alibaba-quark-ocr)
- [ClawHub Publisher Profile](https://clawhub.ai/user/yescan-ai)
- [Quark Scan King Business Platform](https://scan.quark.cn/business)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [JSON returned by the OCR script, usually containing recognized text or structured fields in the data payload.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and SCAN_WEBSERVICE_KEY; accepts exactly one image input as a URL, local file path, or base64 string.]

## Skill Version(s):

1.0.12 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
