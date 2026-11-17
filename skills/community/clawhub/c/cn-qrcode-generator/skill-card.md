## Description:

Generates PNG QR codes from URL or text input using the qrserver.com public API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[freedompixels](https://clawhub.ai/user/freedompixels)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to create QR code images for public URLs or short text. It is useful for producing PNG QR assets with configurable size and, in one script path, foreground and background colors.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: QR content is sent to api.qrserver.com, so secrets, credentials, private internal URLs, tokens, or sensitive personal and business data could be exposed to a third-party service.

Mitigation: Use this skill only for non-sensitive QR content; use a local or offline QR generator when confidentiality is required.

Risk: QR generation depends on an external network service and may fail or return no usable image when that service is unavailable.

Mitigation: Confirm that the generated PNG file or base64 image output is present and valid before using it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/freedompixels/skills/cn-qrcode-generator)
- [QRServer create QR code API](https://api.qrserver.com/v1/create-qr-code/)
- [AISoBrand](https://aisobrand.com)

## Skill Output:

**Output Type(s):** [Text, Code, Shell commands, Files, Guidance]

**Output Format:** [Markdown guidance with shell commands and generated PNG or JSON/base64 output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Calls qrserver.com; default QR size is 300px; output may be a PNG file or base64 image data depending on the script path used.]

## Skill Version(s):

1.2.7 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
