## Description: <br>
Document extraction API by Nanonets. Convert PDFs and images to markdown, JSON, or CSV with confidence scoring. Use when you need to OCR documents, extract invoice fields, parse receipts, or convert tables to structured data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shhdwi](https://clawhub.ai/user/shhdwi) <br>

### License/Terms of Use: <br>
UNLICENSED <br>


## Use Case: <br>
Developers and agents use this skill to call Nanonets DocStrange for OCR and document extraction, including invoices, receipts, contracts, bank statements, forms, and scanned document images. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Uploaded documents are sent to Nanonets external servers for processing and may contain sensitive or regulated data. <br>
Mitigation: Review Nanonets privacy, retention, and compliance terms before use; test with non-sensitive documents first and avoid highly sensitive documents unless the account terms meet the deployment requirements. <br>
Risk: The skill requires a DocStrange API key, and exposing it could allow unauthorized document extraction or account usage. <br>
Mitigation: Store the API key in an environment variable or secret manager, never commit it to repositories, rotate it regularly, and limit permissions where supported. <br>
Risk: Synchronous extraction is documented for documents of five pages or fewer and may time out on larger files. <br>
Mitigation: Use the async extraction endpoint for documents over five pages and poll for results. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shhdwi/docstrange) <br>
- [DocStrange API docs](https://docstrange.nanonets.com/docs) <br>
- [DocStrange dashboard](https://docstrange.nanonets.com/app) <br>
- [Nanonets extraction API endpoint](https://extraction-api.nanonets.com) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API Calls, Markdown, JSON, Text] <br>
**Output Format:** [Markdown guidance with curl examples and JSON response patterns for document extraction outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires DOCSTRANGE_API_KEY and sends selected documents to the Nanonets extraction API.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence; artifact package.json reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
