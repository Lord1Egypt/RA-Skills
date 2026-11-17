## Description:

Quick product image processing: add price sticker + watermark + logo. Use when user sends `$price:` with an image. Minimal context, runs fast.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rueshady](https://clawhub.ai/user/rueshady)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers and agents use this skill to turn product photos into listing-ready images with a price sticker, watermark, and optional logo. The skill is triggered when a user provides `$price:` with an image and produces a processed local image file.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup script can install system packages and modify executable permissions.

Mitigation: Review before installing and run `setup.sh --install` only in an environment where package installation is approved.

Risk: The `--latest` mode scans a default pictures folder when `ECDYSALES_MEDIA_DIR` is not set.

Mitigation: Set `ECDYSALES_MEDIA_DIR` to a narrow staging folder before using `--latest`.

Risk: Advanced options expose a command-execution bug according to the authoritative security guidance.

Mitigation: Avoid exposing user-controlled advanced flags until numeric validation and option allowlisting are fixed.

## Reference(s):

- [ClawHub Ecdysales skill page](https://clawhub.ai/rueshady/skills/ecdysales)
- [ImageMagick](https://imagemagick.org/)
- [HOWTO.md](HOWTO.md)
- [README.md](README.md)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Configuration instructions]

**Output Format:** [Processed image file path and image output; optional JSON status from the CLI]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes processed images to an output directory and can read JSON configuration for sticker, watermark, and logo styling.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
