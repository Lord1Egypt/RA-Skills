## Description:

Recognizes driver's license main and secondary pages and extracts structured fields such as name, certificate number, driving class, issue date, validity period, archive number, and record information.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scnet-sugon](https://clawhub.ai/user/scnet-sugon)

### License/Terms of Use:

MIT

## Use Case:

Agents use this skill to submit driver's license images to Scnet's OCR service and return structured JSON fields for document processing workflows. It is intended for cases where the user has permission to process the identity document.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Driver's license images contain sensitive identity information and are uploaded to Scnet's remote OCR service.

Mitigation: Use the skill only with the document subject's permission and require explicit confirmation before each upload.

Risk: The API endpoint is configurable and the skill sends the API key with each OCR request.

Mitigation: Verify config/.env or environment variables point only to the intended HTTPS Scnet API endpoint, and store SCNET_API_KEY outside chat logs with restricted file permissions.

## Reference(s):

- [Sugon-Scnet OCR API documentation](references/api-docs.md)
- [Driver license output fields](assets/templates/fields-summary.md)
- [Scnet website](https://www.scnet.cn)
- [ClawHub skill page](https://clawhub.ai/scnet-sugon/skills/driver-license-ocr)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Structured JSON printed to standard output, with text error messages for setup, authentication, network, rate-limit, or API failures.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SCNET_API_KEY and optionally SCNET_API_BASE; sends the input file to the configured Scnet OCR API endpoint.]

## Skill Version(s):

1.0.1 (source: frontmatter, skill.yaml, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
