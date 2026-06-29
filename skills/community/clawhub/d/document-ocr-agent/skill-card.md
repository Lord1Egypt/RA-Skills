## Description: <br>
Document OCR Agent extracts text, structured entities, and page-level metadata from PDFs, images, receipts, invoices, and scanned documents through AgentPMT-hosted OCR tool calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agentpmt](https://clawhub.ai/user/agentpmt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and developers use this skill to send a document by URL, AgentPMT file ID, or base64 content and receive OCR text, structured fields, and per-page metadata for document digitization, invoice parsing, receipt processing, and form extraction workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Submitted documents, URLs, or AgentPMT file IDs may contain sensitive or regulated information and are processed through AgentPMT and Google Document AI. <br>
Mitigation: Only submit documents the user is authorized to process, redact unnecessary sensitive data, and avoid passports, driver's licenses, tax forms, bank statements, medical records, and similar documents unless appropriate approvals are in place. <br>
Risk: Requests with more than one input source can fail or process the wrong intended source. <br>
Mitigation: Provide exactly one of file_urls, file_ids, or content_base64 for each process_document request. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/agentpmt/skills/document-ocr-agent) <br>
- [AgentPMT Google Document AI OCR Marketplace Page](https://www.agentpmt.com/marketplace/google-document-ai-ocr) <br>
- [Action Schema](artifact/schema.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, structured entities, metadata, JSON] <br>
**Output Format:** [JSON response containing extracted text, optional entities, page summaries, and optional raw document data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs can be limited with max_text_chars and max_entities; include_pages, include_entities, and include_raw_document control returned detail.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
