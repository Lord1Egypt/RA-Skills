## Description: <br>
Supports OCR recognition for general printed invoices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[scnet-sugon](https://clawhub.ai/user/scnet-sugon) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and agents use this skill to submit a local image or PDF of a general printed invoice to Scnet's OCR API and receive structured invoice fields. It is suited for invoice data extraction workflows that can use a remote OCR service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Invoice files are uploaded to Scnet's external OCR service for processing. <br>
Mitigation: Install and use the skill only when the operator is allowed to send the target invoices to Scnet, and review Scnet's data handling terms before processing confidential invoices. <br>
Risk: The skill requires the sensitive SCNET_API_KEY credential. <br>
Mitigation: Keep SCNET_API_KEY in an environment variable or in a chmod 600 config/.env file, and do not paste the key into chat. <br>
Risk: Repeated OCR calls can encounter API rate limits. <br>
Mitigation: Run requests serially where possible and rely on the skill's retry behavior for 429 responses. <br>


## Reference(s): <br>
- [Sugon-Scnet OCR API documentation](references/api-docs.md) <br>
- [Invoice OCR field summary](assets/templates/fields-summary.md) <br>
- [Scnet website](https://www.scnet.cn) <br>
- [ClawHub release page](https://clawhub.ai/scnet-sugon/general-print-invoice-ocr) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [JSON OCR result data printed to stdout, with text error messages for configuration, authentication, request, or API failures.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SCNET_API_KEY and sends the target invoice file to Scnet's external OCR API.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
