## Description: <br>
Enterprise-grade agentic document processing API that extracts key fields and line items from invoices, receipts, orders, and other document types across 10+ file formats with confidence scoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anna4lucky-stack](https://clawhub.ai/user/anna4lucky-stack) <br>

### License/Terms of Use: <br>
MIT-0; commercial ADP service license required <br>


## Use Case: <br>
Developers, AI agent builders, and enterprise teams use this skill to call Laiye ADP for extracting structured JSON or Excel data from invoices, receipts, purchase orders, financial documents, logistics documents, and multi-table files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends documents to Laiye's external cloud document-processing API and may involve sensitive business documents or personal data. <br>
Mitigation: Confirm organizational approval and ADP privacy, retention, and deletion terms before processing regulated or highly sensitive documents. <br>
Risk: The skill depends on ADP access keys, app keys, and app secrets. <br>
Mitigation: Store credentials in environment variables or a secret manager, avoid committing credentials, rotate keys regularly, and monitor API usage. <br>
Risk: Document extraction can produce incorrect or low-confidence fields. <br>
Mitigation: Review fields with low confidence scores before using extracted values in financial, compliance, or operational workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/anna4lucky-stack/adp-skill) <br>
- [ADP API base URL](https://adp-global.laiye.com/) <br>
- [ADP Product Manual (SaaS)](https://laiye-tech.feishu.cn/wiki/OfexwgVUQiOpEek4kO7c7NEJnAe) <br>
- [Open API User Guide](https://laiye-tech.feishu.cn/wiki/S1t2wYR04ivndKkMDxxcp2SFnKd) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with curl examples and JSON response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documents ADP API calls that return structured extraction results with field-level confidence scores.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
