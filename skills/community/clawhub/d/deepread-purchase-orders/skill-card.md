## Description: <br>
DeepRead Purchase Orders extracts structured purchase order data from PDFs or scans as typed JSON and supports PO-invoice matching with per-field confidence flags. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[uday390](https://clawhub.ai/user/uday390) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Procurement, accounts payable, and finance automation teams use this skill to extract purchase order fields, line items, totals, and review flags from documents. Developers can pair the extracted PO data with invoices or receipts for 2-way or 3-way matching workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Purchase orders and related business data are sent to DeepRead's external API. <br>
Mitigation: Confirm the organization permits this data sharing before installation and route only approved documents through the skill. <br>
Risk: The skill requires a DEEPREAD_API_KEY credential. <br>
Mitigation: Use a scoped key, store it outside shared prompts or source files, and rotate it if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/uday390/deepread-purchase-orders) <br>
- [DeepRead Homepage](https://www.deepread.tech) <br>
- [DeepRead Dashboard](https://www.deepread.tech/dashboard) <br>
- [DeepRead API Endpoint](https://api.deepread.tech) <br>
- [DeepRead Optimizer](https://www.deepread.tech/dashboard/optimizer) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Guidance, Shell commands, Code] <br>
**Output Format:** [Markdown instructions with JSON examples, shell commands, and code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns typed purchase order fields with line items, locations, status, and needs_review confidence flags.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
