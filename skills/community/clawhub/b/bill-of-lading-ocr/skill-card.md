## Description:

Extracts core bill-of-lading fields such as voyage and port details, shipper and consignee names, cargo quantity, bill number, and carrier information using Scnet OCR.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scnet-sugon](https://clawhub.ai/user/scnet-sugon)

### License/Terms of Use:

MIT

## Use Case:

Developers and operations users can invoke this skill to upload an authorized bill-of-lading image, PDF, or supported archive to Scnet OCR and receive structured extraction results for downstream processing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uploads user-selected bill-of-lading files, which may contain commercial or personal data, to an external Scnet OCR service.

Mitigation: Use only files you are authorized to upload and avoid regulated or confidential documents unless your organization has approved Scnet for that data.

Risk: A modified SCNET_API_BASE can redirect documents and the API token away from the documented Scnet endpoint.

Mitigation: Keep SCNET_API_BASE fixed to https://api.scnet.cn/api/llm/v1 or add endpoint validation before use.

## Reference(s):

- [Sugon-Scnet OCR API documentation summary](references/api-docs.md)
- [Bill of lading field summary](assets/templates/fields-summary.md)
- [ClawHub skill release page](https://clawhub.ai/scnet-sugon/skills/bill-of-lading-ocr)
- [Scnet website](https://www.scnet.cn)
- [Scnet OCR recognize endpoint](https://api.scnet.cn/api/llm/v1/ocr/recognize)

## Skill Output:

**Output Type(s):** [JSON, Text]

**Output Format:** [JSON on stdout with human-readable error text on failure]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SCNET_API_KEY and a local file path; uploads the selected file to Scnet OCR.]

## Skill Version(s):

1.0.2 (source: server release metadata, SKILL.md frontmatter, skill.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
