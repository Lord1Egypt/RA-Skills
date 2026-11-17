## Description:

Recognizes Mainland China bank cards and extracts card number, cardholder name, expiration date, and issuing bank information.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scnet-sugon](https://clawhub.ai/user/scnet-sugon)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to send a local bank-card image or document to the Scnet OCR service and receive structured extracted card fields.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bank-card images and related personal or financial data are uploaded to the remote Scnet OCR service.

Mitigation: Use the skill only when the user trusts Scnet with that data, prefers test or redacted cards where possible, and has confirmed privacy and compliance requirements.

Risk: Changing SCNET_API_BASE can send uploads to a different endpoint.

Mitigation: Keep SCNET_API_BASE at the documented https://api.scnet.cn/api/llm/v1 value unless the user intentionally controls and trusts another endpoint.

Risk: The SCNET_API_KEY credential can grant access to the OCR service if exposed.

Mitigation: Store the key outside chat in environment variables or a restricted config file, rotate it if exposed, and run the skill with only the needed files accessible.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/scnet-sugon/skills/bank-card-ocr)
- [Scnet website](https://www.scnet.cn)
- [Sugon-Scnet OCR API documentation summary](references/api-docs.md)
- [Bank-card OCR field summary](assets/templates/fields-summary.md)

## Skill Output:

**Output Type(s):** [JSON, Text, Shell commands, Configuration, Guidance]

**Output Format:** [JSON on stdout with concise text error messages and Markdown usage guidance in the documentation.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SCNET_API_KEY. SCNET_API_BASE is optional and defaults to https://api.scnet.cn/api/llm/v1; the documented service limit is 10 QPS.]

## Skill Version(s):

1.0.6 (source: frontmatter, skill.yaml, ClawHub release metadata, CHANGELOG)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
