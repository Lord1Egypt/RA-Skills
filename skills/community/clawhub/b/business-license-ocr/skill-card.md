## Description:

Extracts structured fields from Chinese mainland business-license images using the Scnet OCR service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scnet-sugon](https://clawhub.ai/user/scnet-sugon)

### License/Terms of Use:

MIT

## Use Case:

External users, employees, and developers use this skill to submit authorized business-license documents and receive structured OCR results such as company name, unified social credit code, legal representative, registered capital, business scope, and address.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Business-license documents are uploaded to the Scnet OCR service and may contain sensitive company identity, address, registration, finance, and operating information.

Mitigation: Process only documents you are authorized to upload, inform users that files leave the local environment, and delete local copies or caches after results are captured when retention is not required.

Risk: The API key and selected document are sent to a configurable remote endpoint.

Mitigation: Keep SCNET_API_BASE set to the documented HTTPS endpoint, store SCNET_API_KEY outside chat transcripts, restrict credential file permissions, and confirm the file path and destination before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/scnet-sugon/skills/business-license-ocr)
- [Scnet website](https://www.scnet.cn)
- [Sugon-Scnet OCR API docs](artifact/references/api-docs.md)
- [Business license OCR field summary](artifact/assets/templates/fields-summary.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [JSON results and concise text guidance for configuration, invocation, and errors.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SCNET_API_KEY and uploads the selected document to the configured Scnet OCR API endpoint.]

## Skill Version(s):

1.0.5 (source: SKILL.md frontmatter, skill.yaml, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
