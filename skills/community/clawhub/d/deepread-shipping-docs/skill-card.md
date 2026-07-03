## Description: <br>
Extract structured data from bills of lading, packing lists, and shipping manifests as typed JSON, including shipper, consignee, carrier, tracking, containers, line items, weights, and per-field confidence flags. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[uday390](https://clawhub.ai/user/uday390) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External logistics, freight, warehouse, customs, and supply-chain teams use this skill to convert shipping documents into structured shipment data for TMS capture, filings, receiving reconciliation, and visibility workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a DeepRead API key and sends documents to the DeepRead API. <br>
Mitigation: Use a scoped key, keep it out of shared logs, and submit only documents approved for third-party processing. <br>
Risk: The authoritative security evidence marks the release suspicious. <br>
Mitigation: Install only in a trusted ClawHub maintainer environment and review the skill before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/uday390/deepread-shipping-docs) <br>
- [DeepRead homepage](https://www.deepread.tech) <br>
- [DeepRead dashboard](https://www.deepread.tech/dashboard) <br>
- [DeepRead optimizer](https://www.deepread.tech/dashboard/optimizer) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, API Calls, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with JSON and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces typed extraction fields with location data and needs_review confidence flags.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
