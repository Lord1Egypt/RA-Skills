## Description:

Generate QR codes from text or URLs for easy sharing and scanning. Outputs as ASCII art or image files for printing and digital use.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dinghaibin](https://clawhub.ai/user/dinghaibin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to generate QR codes for text, URLs, or contact information, and to save them as PNG files or display terminal output for sharing and scanning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documentation advertises ASCII output, but the artifact behavior does not show a working ASCII mode.

Mitigation: Test the required output mode before depending on it, and prefer PNG generation when reliable QR output is needed.

Risk: The tool can read QR codes from image files even though that capability is not described in the public usage section.

Mitigation: Review CLI help and only provide image files that are intended for QR decoding.

Risk: The tool relies on Python QR and image-processing dependencies.

Mitigation: Install dependencies in a virtual environment and use pinned versions from trusted package sources.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dinghaibin/skills/dinghaibin-qrcode-tool)

## Skill Output:

**Output Type(s):** [text, shell commands, files]

**Output Format:** [Markdown or plain text with CLI commands, terminal output, and generated QR image file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce PNG image files when an output path is provided.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
