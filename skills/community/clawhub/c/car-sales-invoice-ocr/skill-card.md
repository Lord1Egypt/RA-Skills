## Description:

Supports precise extraction of vehicle-specific fields from motor vehicle sales invoices, including VIN, engine number, brand model, buyer information, total tax-inclusive amount, and tax payment voucher number.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scnet-sugon](https://clawhub.ai/user/scnet-sugon)

### License/Terms of Use:

MIT

## Use Case:

External users and agents use this skill to submit local motor vehicle sales invoice images, PDFs, or archives to the Sugon-Scnet OCR API and receive structured invoice fields for downstream review or processing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Vehicle sales invoices may contain sensitive buyer, seller, tax, and vehicle identifiers that are uploaded to an external OCR endpoint.

Mitigation: Use the skill only after confirming that upload to Sugon-Scnet or another approved OCR endpoint is allowed for the invoice data, and redact or withhold documents when consent, policy, or vendor review is required.

Risk: A configurable API base can direct invoice files and bearer-token requests away from the documented Scnet host.

Mitigation: Keep SCNET_API_BASE set to the documented HTTPS Scnet API base unless an alternate endpoint has been explicitly reviewed and approved.

Risk: The required SCNET_API_KEY is stored in local configuration and used as a bearer token for network requests.

Mitigation: Protect the .env file, avoid pasting API keys into chat, rotate expired or exposed tokens, and restrict file permissions to the local owner.

Risk: The OCR API has documented rate limits, and repeated concurrent calls can cause 429 failures.

Mitigation: Call the skill serially or throttle batch workflows, and retry only after an appropriate delay when rate limits are encountered.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/scnet-sugon/skills/car-sales-invoice-ocr)
- [Publisher Profile](https://clawhub.ai/user/scnet-sugon)
- [Sugon-Scnet OCR API Documentation Summary](references/api-docs.md)
- [Vehicle Sales Invoice Fields Summary](assets/templates/fields-summary.md)
- [Scnet Website](https://www.scnet.cn)
- [Scnet OCR API Base](https://api.scnet.cn/api/llm/v1)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [JSON data on standard output with human-facing error text for configuration, network, or API failures.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Recognized invoice data is returned from the API data payload after removing confidence fields; output fields vary by OCR type.]

## Skill Version(s):

1.0.3 (source: frontmatter, skill.yaml, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
