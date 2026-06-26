## Description: <br>
ADP Global Invoice Extraction Free API sends invoices and receipts to Laiye ADP public cloud endpoints and returns structured JSON extraction results across 100+ languages and international formats. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[laiye-adp](https://clawhub.ai/user/laiye-adp) <br>

### License/Terms of Use: <br>
Commercial License Agreement <br>


## Use Case: <br>
Finance teams, automation builders, and system integrators use this skill to extract invoice and receipt fields from scanned images, PDFs, and public file URLs for reconciliation, data entry, and downstream workflow automation. <br>

### Deployment Geography for Use: <br>
Global and China regional public cloud endpoints. <br>

## Known Risks and Mitigations: <br>
Risk: Invoices and receipts can contain confidential or regulated data, and this skill submits selected documents or public file URLs to Laiye-operated cloud APIs. <br>
Mitigation: Submit only documents you are authorized to share, and avoid confidential, regulated, customer, employee, tax, or payment documents unless Laiye data handling, retention, regional processing, and compliance terms have been reviewed. <br>
Risk: The free API has file size, page count, format, and rate limits that can reject production-scale or multi-page workflows. <br>
Mitigation: Validate file size, page count, format, and URL accessibility before requests; handle 400 and 429 responses or use a full ADP account when higher quotas or broader document support are required. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/laiye-adp/adp-global-invoice-extraction-free) <br>
- [Open API User Guide](https://laiye-tech.feishu.cn/wiki/S1t2wYR04ivndKkMDxxcp2SFnKd) <br>
- [ADP Product Manual](https://laiye-tech.feishu.cn/wiki/OfexwgVUQiOpEek4kO7c7NEJnAe) <br>
- [ADP CLI User Guide](https://laiye-tech.feishu.cn/wiki/YIaawiK2DimisZk5KfDc8a8cnLh) <br>
- [Laiye ADP Platform](https://laiye.com/en/product/adp-platform) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, API calls, Shell commands, Code, Guidance] <br>
**Output Format:** [Markdown guidance with curl and Python examples; API responses are structured JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Accepts a public file URL or base64-encoded document; free endpoint limits include single-page files under 2 MB and documented per-IP/global request quotas.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
