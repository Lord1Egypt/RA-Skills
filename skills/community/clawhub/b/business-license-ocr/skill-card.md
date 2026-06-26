## Description: <br>
Recognizes mainland China business licenses with Sugon-Scnet OCR and extracts structured fields such as unified social credit code, company name, legal representative, registered capital, establishment date, business scope, and address. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[scnet-sugon](https://clawhub.ai/user/scnet-sugon) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to send a local business-license image, PDF, or archive to the Scnet OCR API and receive structured JSON fields for review, data entry, or downstream automation. <br>

### Deployment Geography for Use: <br>
Global; intended document type is mainland China business licenses. <br>

## Known Risks and Mitigations: <br>
Risk: Selected documents are sent to an external Scnet OCR API and may include sensitive business or identity information. <br>
Mitigation: Confirm the file path, document type, and endpoint before use; avoid routing IDs, invoices, or other sensitive documents unless that broader processing is intentional and acceptable under privacy requirements. <br>
Risk: The skill requires an SCNET_API_KEY credential for API access. <br>
Mitigation: Store the credential in the documented environment variable or local .env file with restricted permissions, and do not paste API keys into chat. <br>


## Reference(s): <br>
- [Sugon-Scnet OCR API Documentation Summary](artifact/references/api-docs.md) <br>
- [Business License Field Summary](artifact/assets/templates/fields-summary.md) <br>
- [Scnet Website](https://www.scnet.cn) <br>
- [ClawHub Skill Page](https://clawhub.ai/scnet-sugon/business-license-ocr) <br>


## Skill Output: <br>
**Output Type(s):** [json, text, shell commands, configuration] <br>
**Output Format:** [JSON data on stdout with human-readable error text on failure] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SCNET_API_KEY and sends selected files to the Scnet OCR API; the skill documents a 10 QPS rate limit and retry behavior.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release, SKILL.md frontmatter, skill.yaml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
