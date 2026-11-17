## Description:

Generate brat-style text cover images and sticker-like WhatsApp-safe outputs from custom text.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sqizzo](https://clawhub.ai/user/sqizzo)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate brat-style text cover images, parse !brat command input, and prepare PNG-first sticker-like image outputs for WhatsApp-style delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted workspace users could interfere with generated files in the managed scripts/out directory.

Mitigation: Install only in trusted workspaces and avoid letting untrusted users write inside the skill's scripts/out directory.

Risk: Very large image sizes or text inputs could cause unnecessary local resource use.

Mitigation: Use normal, user-approved output paths and reasonable image sizes and text lengths.

Risk: WhatsApp delivery may send generated files as image media rather than verified native stickers.

Mitigation: Use PNG sticker-like image delivery unless the outbound layer is verified to support native sticker payloads.

## Reference(s):

- [Delivery Notes](references/delivery-notes.md)
- [ClawHub skill page](https://clawhub.ai/sqizzo/skills/bratification)

## Skill Output:

**Output Type(s):** [Files, JSON, Shell commands, Guidance]

**Output Format:** [PNG and WEBP image files, JSON path metadata, and Markdown command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [PNG is the primary delivery format; WEBP is optional until native sticker upload support is verified.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
