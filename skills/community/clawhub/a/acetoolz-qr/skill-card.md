## Description:

Generate QR codes for any URL or text instantly using AceToolz and return a hosted image URL ready to share in chat.

This skill is ready for commercial/non-commercial use.

## Publisher:

[acetoolz](https://clawhub.ai/user/acetoolz)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to generate a QR code for supplied text or a URL and return a shareable hosted image link.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The content or URL to encode is sent to AceToolz for QR generation.

Mitigation: Do not use the skill for passwords, tokens, private internal links, or sensitive personal data unless third-party handling is acceptable.

Risk: The primary result is a hosted image URL controlled by the third-party service.

Mitigation: Review the generated link before sharing it in contexts where persistence, branding, or external hosting matters.

## Reference(s):

- [AceToolz QR Generator](https://www.acetoolz.com/generate/tools/qr-generator)
- [ClawHub Skill Page](https://clawhub.ai/acetoolz/skills/acetoolz-qr)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown response with a hosted QR image URL and optional data URL details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Calls the AceToolz QR API with content and size parameters; primary user-facing result is qr_image_url.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
