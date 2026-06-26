## Description: <br>
Parse EDI X12 files (810 Invoice, 850 Purchase Order, 856 ASN). Extract structured data from ISA/GS envelopes, transaction sets, and segments. Use when working with EDI files, Walmart/retail supplier compliance, or extracting PO, invoice, and shipment data from X12 format. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[npfaerber](https://clawhub.ai/user/npfaerber) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, analysts, and retail supplier teams use this skill to inspect EDI X12 810, 850, and 856 documents and extract envelope, purchase order, invoice, shipment, and line-item details into readable tables or CSV output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: EDI documents can contain sensitive supplier, invoice, shipment, and customer-location data. <br>
Mitigation: Provide only files or excerpts that are appropriate for the agent to process, and redact unnecessary sensitive values before sharing. <br>
Risk: Incorrect extraction could misstate purchase order, invoice, shipment, or line-item details. <br>
Mitigation: Review parsed tables or CSV output against the source EDI before using the results for compliance, fulfillment, or financial decisions. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, CSV, Guidance] <br>
**Output Format:** [Markdown table for single documents or CSV rows for bulk line-item parsing] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs extracted EDI fields such as transaction type, ISA sender and receiver, purchase order, ship date, totals, and item counts when present.] <br>

## Skill Version(s): <br>
1.0.1 (source: server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
