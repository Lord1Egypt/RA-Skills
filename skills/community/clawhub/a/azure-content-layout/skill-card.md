## Description: <br>
Extracts document structure, text, tables, and figures from PDFs, images, Office documents, and HTML using Azure Content Understanding prebuilt-layout analyzer. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zwcih](https://clawhub.ai/user/zwcih) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and document-processing agents use this skill to convert user-selected documents or URLs into Markdown and structured JSON for downstream analysis, OCR workflows, table extraction, and layout-aware document review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill submits user-selected document URLs or stdin document bytes to a configured Azure Content Understanding endpoint. <br>
Mitigation: Use a dedicated Azure key and trusted endpoint, and only process confidential, regulated, secret-bearing, or internal-only documents when organizational policy permits Azure processing for that data. <br>
Risk: Document extraction output may be incomplete or inaccurate for complex layouts, large files, or failed Azure analysis jobs. <br>
Mitigation: Review generated Markdown and JSON before relying on the extracted content in downstream decisions or publications. <br>


## Reference(s): <br>
- [Azure Content Understanding Layout API Reference](references/api.md) <br>
- [ClawHub release page](https://clawhub.ai/zwcih/azure-content-layout) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration] <br>
**Output Format:** [Markdown and structured JSON, with setup guidance and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AZURE_CU_ENDPOINT, AZURE_CU_API_KEY, and optionally AZURE_CU_API_VERSION.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
