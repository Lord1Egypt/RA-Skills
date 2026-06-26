## Description: <br>
Agent Paddleocr Vision provides multi-language document understanding with PaddleOCR cloud OCR. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[NHZallen](https://clawhub.ai/user/NHZallen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to OCR images and PDFs, classify document types, extract structured fields, and generate suggested next actions for document workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Documents are uploaded to the configured PaddleOCR endpoint and generated outputs may contain sensitive information. <br>
Mitigation: Install only when the endpoint is trusted, uploads are approved for the document class, access tokens are protected, and outputs are stored securely. <br>
Risk: Suggested actions may involve financial, identity, contact, calendar, or record-keeping decisions. <br>
Mitigation: Require human confirmation before acting on suggested actions or using extracted fields in downstream systems. <br>
Risk: OCR, classification, and bounding-box alignment can be incomplete or inaccurate. <br>
Mitigation: Review extracted text, structured fields, confidence values, and generated searchable PDFs before relying on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/NHZallen/agent-paddleocr-vision) <br>
- [Project homepage](https://github.com/NHZallen/agent-paddleocr-vision) <br>
- [English documentation](docs/README.en.md) <br>
- [PaddleOCR API guide](https://paddleocr.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance, files] <br>
**Output Format:** [JSON, text, pretty text, CSV, and optional searchable PDF files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs can include extracted text, document type confidence, structured fields, suggested actions, batch summaries, and searchable PDF paths.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
