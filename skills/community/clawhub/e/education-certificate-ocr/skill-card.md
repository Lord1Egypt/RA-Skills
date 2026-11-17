## Description:

Recognizes education certificates and extracts structured fields such as holder name, certificate number, major, institution, graduation date, and confidence data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scnet-sugon](https://clawhub.ai/user/scnet-sugon)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to send local education certificate images, PDFs, or archives to the Scnet OCR service and receive structured JSON extraction results for downstream review or processing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Certificate images, PDFs, archives, and extracted personal information are uploaded to a remote OCR service.

Mitigation: Confirm each sensitive file before use and install the skill only when sending this data to Scnet is acceptable.

Risk: The API credential is read from local configuration and sent with OCR requests.

Mitigation: Keep config/.env private, restrict file permissions, and never paste the API key into chat or shared logs.

Risk: The optional SCNET_API_BASE setting can redirect requests to a different endpoint.

Mitigation: Change SCNET_API_BASE only after verifying that the destination is trusted and expected.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/scnet-sugon/skills/education-certificate-ocr)
- [Publisher profile](https://clawhub.ai/user/scnet-sugon)
- [Scnet website](https://www.scnet.cn)
- [Sugon-Scnet OCR API docs](artifact/references/api-docs.md)
- [Education certificate fields summary](artifact/assets/templates/fields-summary.md)

## Skill Output:

**Output Type(s):** [JSON, API Calls, Shell commands, Guidance]

**Output Format:** [Structured JSON printed to standard output, with human-facing error messages for configuration, authentication, network, and rate-limit failures.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SCNET_API_KEY and accepts an optional SCNET_API_BASE endpoint override.]

## Skill Version(s):

1.0.0 (source: frontmatter, skill.yaml, changelog, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
