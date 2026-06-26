## Description: <br>
Recognizes fixed-amount invoices by sending a user-provided file to the Scnet OCR API and returning structured OCR data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[scnet-sugon](https://clawhub.ai/user/scnet-sugon) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to extract key fields from fixed-amount invoice images, PDFs, or archives through Scnet's OCR service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Invoice files are sent to Scnet's OCR service for processing. <br>
Mitigation: Use the skill only with invoice files that are approved for processing by Scnet's service and comply with the user's data-handling requirements. <br>
Risk: The skill requires SCNET_API_KEY, which could be exposed if pasted into chat or stored with broad permissions. <br>
Mitigation: Provide the key through an environment variable or a permission-restricted config/.env file, and do not paste the key into chat. <br>
Risk: Server-resolved provenance is unavailable and the security summary notes documentation and metadata inconsistencies. <br>
Mitigation: Verify the publisher profile and Scnet service endpoints before installing or using the skill. <br>
Risk: The OCR API can rate-limit requests. <br>
Mitigation: Run OCR calls serially and allow retry/backoff behavior before submitting additional requests. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/scnet-sugon/fixed-amount-invoice-ocr) <br>
- [Sugon-Scnet OCR API Documentation Summary](references/api-docs.md) <br>
- [Fixed-Amount Invoice Field Summary](assets/templates/fields-summary.md) <br>
- [Scnet](https://www.scnet.cn) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Text, Shell commands] <br>
**Output Format:** [JSON on standard output with plain-text error messages on failure] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SCNET_API_KEY and uploads the specified local invoice file to Scnet's OCR API.] <br>

## Skill Version(s): <br>
1.0.4 (source: SKILL.md frontmatter and ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
