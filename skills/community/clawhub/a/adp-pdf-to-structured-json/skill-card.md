## Description: <br>
A Laiye ADP document-processing skill that guides an agent through parsing PDFs, images, scanned documents, and Office files into structured JSON. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[laiye-adp](https://clawhub.ai/user/laiye-adp) <br>

### License/Terms of Use: <br>
Commercial License Agreement <br>


## Use Case: <br>
Developers, analysts, and automation teams use this skill to convert business documents into structured JSON for storage, retrieval, ETL pipelines, quality inspection, and cross-system integration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected documents or URLs are processed by Laiye ADP cloud services and may contain sensitive, regulated, customer, or confidential data. <br>
Mitigation: Use the skill only when authorized for the document contents and avoid submitting contracts, IDs, invoices, secrets, regulated records, or customer data without approval. <br>
Risk: The skill requires an ADP API key and service configuration. <br>
Mitigation: Protect the API key, prefer environment variables or the documented encrypted configuration storage, and check configuration before parsing documents. <br>
Risk: Optional remote installer commands pipe downloaded scripts into a shell. <br>
Mitigation: Prefer the npm package or verified release binaries, and review remote installer scripts before execution when those alternatives are not available. <br>
Risk: Document parsing uses credits and can incur usage-based costs, especially for batch or async workflows. <br>
Mitigation: Check available credits before large jobs, monitor billing, and confirm batch scope before submitting many documents. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/laiye-adp/adp-pdf-to-structured-json) <br>
- [Laiye ADP global portal](https://adp-global.laiye.com/?utm_source=clawhub) <br>
- [Laiye ADP mainland China portal](https://adp.laiye.com/?utm_source=clawhub) <br>
- [ADP CLI releases](https://github.com/laiye-ai/adp-cli/releases) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with ADP CLI commands and structured JSON results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports local files, URLs, Base64 input, batch jobs, async task queries, exported result files, OCR confidence fields, and document element positions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
