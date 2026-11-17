## Description:

Recognizes degree certificate images or PDFs and extracts structured fields such as certificate holder, university, major, degree, certificate number, issue date, and confidence-related result data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scnet-sugon](https://clawhub.ai/user/scnet-sugon)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to send degree certificate files to the Scnet OCR service and receive structured recognition results for downstream review, record extraction, or workflow automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Degree certificates can contain personal data, and the security evidence notes that files are uploaded to Scnet or the configured API base.

Mitigation: Use the skill only with appropriate consent, avoid uploading unnecessary sensitive certificates, and keep SCNET_API_BASE at the documented HTTPS Scnet endpoint unless another server is intentionally trusted.

Risk: The skill requires SCNET_API_KEY for remote OCR access.

Mitigation: Protect the API key in environment variables or config/.env with restricted permissions, and do not paste credentials into chats or shared logs.

Risk: The documented OCR service has request-rate limits.

Mitigation: Call the skill serially for batches and retry later when rate-limit errors persist.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/scnet-sugon/skills/degree-certificate-ocr)
- [Sugon-Scnet OCR API documentation](references/api-docs.md)
- [Degree certificate OCR fields](assets/templates/fields-summary.md)
- [Scnet website](https://www.scnet.cn)

## Skill Output:

**Output Type(s):** [text]

**Output Format:** [JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The JSON contains OCR recognition data returned from the Scnet service, with fields varying by OCR type.]

## Skill Version(s):

1.0.0 (source: frontmatter, skill.yaml, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
