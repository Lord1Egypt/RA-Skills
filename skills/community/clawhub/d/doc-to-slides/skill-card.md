## Description:

Convert documents or text into PDF slide presentations via the Ruyi Converter API at nyoi.io.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lisiting01](https://clawhub.ai/user/lisiting01)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to turn notes, markdown, PDFs, DOCX files, TXT files, or other presentation source material into PDF slide decks through a third-party conversion service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Presentation source material is sent to the third-party nyoi.io service.

Mitigation: Avoid confidential, regulated, or proprietary documents unless the service provider's retention and access controls are acceptable.

Risk: API keys, job IDs, and generated download links are sensitive and may expose submitted content or results.

Mitigation: Treat credentials, job identifiers, and pre-signed URLs as secrets; do not print full credentials or links unless necessary for delivery.

Risk: Download links expire after 2 hours, while the API reference states files are not deleted when links expire.

Mitigation: Deliver the PDF as a file attachment promptly and request a fresh job artifact URL if the original link expires.

## Reference(s):

- [Doc2Slides ClawHub Listing](https://clawhub.ai/lisiting01/skills/doc-to-slides)
- [Ruyi Converter API Reference](references/api-reference.md)
- [Ruyi Converter Service](https://www.nyoi.io)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Guidance]

**Output Format:** [PDF slide deck delivered as a file attachment, with Markdown guidance and inline shell command examples for the agent workflow]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The generated PDF is exposed through a pre-signed download link that is valid for 2 hours; large jobs can take up to 30 minutes.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
