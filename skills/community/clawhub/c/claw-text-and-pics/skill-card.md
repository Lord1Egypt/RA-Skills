## Description: <br>
Extract text and embedded images from scanned documents, PDFs, and photos via the Mistral OCR API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[photon78](https://clawhub.ai/user/photon78) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to extract Markdown text from scanned invoices, receipts, contracts, handwritten notes, PDFs, and images, with optional embedded-image extraction and Telegram delivery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Documents submitted for OCR are sent to Mistral, which may expose sensitive or regulated content to an external service. <br>
Mitigation: Use the skill only with documents approved for external OCR processing and store the Mistral API key securely. <br>
Risk: Using --send can share extracted images through Telegram with the configured chat. <br>
Mitigation: Enable --send only after verifying the Telegram bot token and target chat ID, and only for images intended to be shared externally. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/photon78/claw-text-and-pics) <br>
- [Publisher profile](https://clawhub.ai/user/photon78) <br>
- [Mistral OCR API documentation](https://docs.mistral.ai/capabilities/document/) <br>
- [OpenClaw](https://openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, shell commands, configuration] <br>
**Output Format:** [Markdown text on stdout with optional JPEG image files and optional Telegram photo messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Mistral API key; image extraction requires Pillow and local input files; Telegram sending requires a bot token and target chat ID.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
