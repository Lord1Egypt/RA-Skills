## Description:

Extract structured data from bills of lading, packing lists, and shipping manifests, including shipper, consignee, carrier, tracking, containers, line items, weights, and per-field confidence flags, as typed JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[uday390](https://clawhub.ai/user/uday390)

### License/Terms of Use:

MIT-0

## Use Case:

Logistics, customs, warehouse, and supply-chain teams use this skill to extract machine-readable shipment data from bills of lading, packing lists, and manifests for downstream review, reconciliation, or filing workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Shipping documents may contain confidential, private, regulated, or commercially sensitive information and are uploaded to DeepRead for extraction.

Mitigation: Confirm organizational approval and review DeepRead data handling and retention terms before uploading bills of lading, manifests, packing lists, or similarly sensitive documents.

Risk: Extracted fields can be uncertain, especially for handwritten weights or quantities.

Mitigation: Use the per-field needs_review flags and human review before relying on extracted values for filings, reconciliation, or operational decisions.

## Reference(s):

- [DeepRead homepage](https://www.deepread.tech)
- [DeepRead dashboard](https://www.deepread.tech/dashboard)
- [DeepRead dashboard signup](https://www.deepread.tech/dashboard/?utm_source=clawhub)
- [DeepRead optimizer](https://www.deepread.tech/dashboard/optimizer)
- [DeepRead API endpoint](https://api.deepread.tech/v1/process)
- [ClawHub skill page](https://clawhub.ai/uday390/skills/deepread-shipping-docs)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Typed JSON extraction results with Markdown setup and cURL examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires DEEPREAD_API_KEY and user-selected shipping documents; results include needs_review flags for extracted fields.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
