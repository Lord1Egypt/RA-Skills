## Description: <br>
Extracts structured data from invoices, receipts, bills, and purchase orders using DeepRead, including vendor details, line items, totals, taxes, due dates, and human-review confidence flags. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[uday390](https://clawhub.ai/user/uday390) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operations teams, and finance workflows use this skill to submit invoice-like documents to DeepRead and receive structured JSON for accounts payable, receipt processing, purchase-order matching, bookkeeping, and audit review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Invoices, receipts, and bills may contain sensitive financial, vendor, tax, or personal data that is sent to DeepRead and any configured BYOK model provider. <br>
Mitigation: Use the skill only when authorized to process those documents, review DeepRead and provider privacy, retention, data residency, and compliance terms, and test with redacted or non-sensitive documents before production use. <br>
Risk: Extracted fields can be incorrect or uncertain, especially where the service marks fields for human-in-the-loop review. <br>
Mitigation: Route fields with review flags to a human reviewer and validate extracted totals, dates, vendors, and line items before accounting, payment, or audit actions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/uday390/deepread-invoice) <br>
- [DeepRead Homepage](https://www.deepread.tech) <br>
- [DeepRead Dashboard](https://www.deepread.tech/dashboard) <br>
- [DeepRead BYOK Setup](https://www.deepread.tech/dashboard/byok) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown guidance with Python, cURL, environment-variable setup, and JSON schema examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires DEEPREAD_API_KEY and sends user-selected documents to the DeepRead API; returned fields may include human-in-the-loop review flags.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
