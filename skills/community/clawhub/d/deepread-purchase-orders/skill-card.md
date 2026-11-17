## Description:

Extract structured data from purchase orders -- PO number, buyer/supplier, line items, quantities, prices, delivery dates, totals -- as typed JSON, with 2-way/3-way matching against invoices and per-field confidence flags.

This skill is ready for commercial/non-commercial use.

## Publisher:

[uday390](https://clawhub.ai/user/uday390)

### License/Terms of Use:

MIT-0

## Use Case:

Procurement, AP, and operations teams use this skill to extract structured purchase-order fields from PDF or scanned documents, then compare purchase orders with invoices and receipts for review workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Purchase-order documents may contain sensitive supplier, buyer, pricing, and delivery information that is sent to DeepRead's hosted API.

Mitigation: Review DeepRead's data handling terms and only submit documents appropriate for that hosted service.

Risk: The skill requires a DEEPREAD_API_KEY for API access.

Mitigation: Store the key in a managed environment variable or secret store and avoid committing it to source files or logs.

## Reference(s):

- [DeepRead homepage](https://www.deepread.tech)
- [DeepRead dashboard](https://www.deepread.tech/dashboard)
- [ClawHub skill page](https://clawhub.ai/uday390/skills/deepread-purchase-orders)

## Skill Output:

**Output Type(s):** [JSON, API Calls, Configuration instructions, Guidance]

**Output Format:** [Typed JSON with setup commands and reconciliation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires DEEPREAD_API_KEY and sends user-provided purchase-order documents to DeepRead's hosted API.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
