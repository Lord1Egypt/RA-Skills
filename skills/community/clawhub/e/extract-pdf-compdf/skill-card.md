## Description: <br>
PDF Extract helps agents process PDFs and images through ComPDF Cloud for OCR, structured extraction, conversion, page editing, compression, comparison, and export workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[compdf-youna](https://clawhub.ai/user/compdf-youna) <br>

### License/Terms of Use: <br>
Apache 2.0 <br>


## Use Case: <br>
Developers, analysts, and automation users use this skill when they need an agent to extract tables or text, run OCR, convert files, edit PDF pages, or return downloadable ComPDF processing results from user-selected documents. <br>

### Deployment Geography for Use: <br>
Global, with International and Mainland China API endpoints selected according to the user's environment. <br>

## Known Risks and Mitigations: <br>
Risk: Selected documents, and encrypted-PDF passwords when supplied, are uploaded to ComPDF's cloud service for processing. <br>
Mitigation: Require explicit user confirmation before upload and avoid highly sensitive documents unless the user's ComPDF account, privacy requirements, and data-handling obligations allow it. <br>
Risk: The skill covers extraction, conversion, and PDF editing operations, so an incorrect operation or parameter choice could process unintended pages or produce an unexpected output. <br>
Mitigation: Review the requested operation, tool type, page ranges, and optional parameters with the user before sending the request. <br>
Risk: A ComPDF API key can be stored locally if the user opts in. <br>
Mitigation: Store the key only after explicit user approval, use it only for ComPDF requests, and remind the user they can delete the local key file. <br>


## Reference(s): <br>
- [ComPDF API Overview](https://www.compdf.com/guides/api-reference/v2/overview?utm_source=clawhub&utm_medium=skillhub&utm_campaign=pdf_skill_pdf_extract&ref_platform_id=clawhub_skills) <br>
- [ComPDF API Complete Tool Type Reference](references/tool-list.md) <br>
- [ComPDF API Tool Parameter Details](references/parameters.md) <br>
- [ComPDF API Error Code Reference](references/error-codes.md) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Markdown, JSON, Files, Guidance] <br>
**Output Format:** [Markdown status summaries with API response fields, troubleshooting guidance, and download URLs for processed files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a ComPDF API key, explicit upload confirmation, selected operation, source documents, and optional JSON parameters for supported tools.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
