## Description: <br>
Recognizes mainland China bank cards and extracts card number, cardholder name, expiry date, issuing bank information, and OCR confidence data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[scnet-sugon](https://clawhub.ai/user/scnet-sugon) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and external users use this skill to send a local bank-card image or document to the Sugon-Scnet OCR API and receive structured card fields for downstream review or processing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bank-card images and extracted payment-card details are sensitive and are uploaded to SCNet for OCR. <br>
Mitigation: Run the skill only with explicit approval, prefer test or approved images, and confirm the data handling and compliance posture before using real payment-card data. <br>
Risk: The skill requires an SCNET_API_KEY credential. <br>
Mitigation: Store the key in the configured environment or local .env file, restrict file permissions, rotate expired keys, and do not paste the key into chat. <br>
Risk: Publisher provenance is unavailable in the server-resolved evidence. <br>
Mitigation: Verify the SCNet publisher profile and source before deployment or use with sensitive card data. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/scnet-sugon/bank-card-ocr) <br>
- [Sugon-Scnet OCR API Documentation Summary](references/api-docs.md) <br>
- [Bank Card Field Summary](assets/templates/fields-summary.md) <br>
- [SCNet Website](https://www.scnet.cn) <br>
- [SCNet OCR API Endpoint](https://api.scnet.cn/api/llm/v1/ocr/recognize) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, API Calls, Shell commands, Configuration] <br>
**Output Format:** [Structured JSON returned on standard output, with friendly error text for failures.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SCNET_API_KEY; uploads the selected image or document to SCNet and may retry rate-limited requests.] <br>

## Skill Version(s): <br>
1.0.6 (source: SKILL.md frontmatter, skill.yaml, release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
