## Description:

Recognizes bus ticket receipts with the Sugon-Scnet OCR service and returns structured ticket fields.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scnet-sugon](https://clawhub.ai/user/scnet-sugon)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to send a local bus ticket image, PDF, or archive to Scnet's OCR API and receive structured ticket data such as route, dates, invoice numbers, passenger name, and amount.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bus ticket images, PDFs, or archives may contain passenger names, routes, dates, invoice numbers, and amounts that are uploaded to Scnet's OCR service.

Mitigation: Use the skill only where sending those documents to Scnet is acceptable, and have the agent confirm before each upload.

Risk: SCNET_API_BASE can change the upload endpoint.

Mitigation: Keep the default Scnet API base unless the replacement endpoint is controlled and trusted.

Risk: A configured Scnet API key can be exposed if config/.env is readable by untrusted users or pasted into chat.

Mitigation: Prefer environment variables or restrict config/.env permissions to trusted users, and never share the API key in conversation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/scnet-sugon/skills/bus-ticket-ocr)
- [Sugon-Scnet OCR API documentation summary](artifact/references/api-docs.md)
- [Bus ticket field summary](artifact/assets/templates/fields-summary.md)
- [Scnet website](https://www.scnet.cn)

## Skill Output:

**Output Type(s):** [text, JSON]

**Output Format:** [Pretty-printed JSON on standard output, with human-readable error text on failure.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The script removes confidence fields from successful API results before printing the data array.]

## Skill Version(s):

1.0.3 (source: frontmatter, skill.yaml, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
