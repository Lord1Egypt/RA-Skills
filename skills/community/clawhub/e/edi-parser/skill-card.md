## Description:

Parse EDI X12 files (810 Invoice, 850 Purchase Order, 856 ASN). Extract structured data from ISA/GS envelopes, transaction sets, and segments. Use when working with EDI files, Walmart/retail supplier compliance, or extracting PO, invoice, and shipment data from X12 format.

This skill is ready for commercial/non-commercial use.

## Publisher:

[npfaerber](https://clawhub.ai/user/npfaerber)

### License/Terms of Use:


## Use Case:

Developers, engineers, and retail operations teams use this skill to interpret user-provided EDI X12 invoices, purchase orders, and advance ship notices and summarize key envelope, transaction, shipment, invoice, and line-item fields.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: EDI files can contain purchase orders, shipment details, invoice amounts, vendor numbers, and trading partner identifiers.

Mitigation: Use the skill only with EDI files that are appropriate to share with the agent session, and review generated summaries before relying on them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/npfaerber/skills/edi-parser)
- [ClawHub publisher profile](https://clawhub.ai/user/npfaerber)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown tables or CSV-style tabular summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Summaries are derived from user-provided EDI content; bulk parsing may produce one row per line item.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
