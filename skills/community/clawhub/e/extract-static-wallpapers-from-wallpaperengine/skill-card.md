## Description:

Extracts static PNG wallpapers, including mipmap resolution levels, from Wallpaper Engine scene.pkg files in PKGV0023/PKGV0024 format.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pandhumhp-cn](https://clawhub.ai/user/pandhumhp-cn)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to extract Wallpaper Engine package contents from a supplied scene.pkg file, recover embedded PNG images from .tex textures, and identify the largest wallpaper image for delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A malicious scene.pkg package may cause extracted files to be written outside the selected output directory.

Mitigation: Run the extractor only on trusted scene.pkg files in a disposable low-privilege working directory until entry paths are validated and writes are confined to the output directory.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pandhumhp-cn/skills/extract-static-wallpapers-from-wallpaperengine)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Guidance]

**Output Format:** [Markdown guidance with shell command snippets and extracted PNG file attachments]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce multiple PNG mipmap files and extracted package contents.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
