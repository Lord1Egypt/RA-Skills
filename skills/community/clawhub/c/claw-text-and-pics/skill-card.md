## Description:

Extract text and embedded images from scanned documents, PDFs, and photos via Mistral OCR API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[photon78](https://clawhub.ai/user/photon78)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to extract Markdown text from scanned receipts, invoices, contracts, handwritten notes, images, and PDFs. When requested, it can crop embedded images from local documents and optionally send extracted images through Telegram.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected documents are uploaded to Mistral for OCR processing.

Mitigation: Use the skill only with documents you are permitted to send to Mistral, and avoid confidential, regulated, or third-party material unless approved.

Risk: Using --send uploads extracted images to Telegram.

Mitigation: Use --send only intentionally, confirm the Telegram target, and configure Telegram credentials only for approved destinations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/photon78/skills/claw-text-and-pics)
- [Mistral OCR API documentation](https://docs.mistral.ai/capabilities/document/)
- [OpenClaw](https://openclaw.ai)

## Skill Output:

**Output Type(s):** [text, markdown, files, shell commands, configuration, guidance]

**Output Format:** [Markdown text on stdout, optional JPEG image files, and optional Telegram photo messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MISTRAL_API_KEY; Pillow is required only for image extraction; Telegram credentials are required only when using --send.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
