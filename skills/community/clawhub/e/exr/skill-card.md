## Description:

Work with OpenEXR files to inspect channels, extract beauty/RGB passes, decode cryptomatte segmentation, convert ACEScg to sRGB, and batch process EXR directories.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oumad](https://clawhub.ai/user/oumad)

### License/Terms of Use:


## Use Case:

Developers, technical artists, and rendering engineers use this skill to inspect OpenEXR render outputs, extract RGB or arbitrary channel images, and generate cryptomatte segmentation PNGs for compositing, review, or dataset preparation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The pinned OpenEXR parser is known-vulnerable and is directly exposed to EXR files opened by the user.

Mitigation: Review before installing, run in an isolated virtual environment, and avoid untrusted EXR files unless OpenEXR is updated to a patched compatible release.

Risk: Dependency integrity is not fully locked because numpy and Pillow are not pinned with reviewed versions and hashes.

Mitigation: Lock numpy and Pillow to reviewed versions with hashes before production or shared-environment use.

## Reference(s):

- [Color Space Reference](references/color-spaces.md)
- [Cryptomatte Format Reference](references/cryptomatte.md)
- [Usage Examples](references/usage.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files]

**Output Format:** [Markdown guidance with shell commands and Python examples; CLI execution can produce PNG image files and terminal text output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and the packaged Python dependencies before using the EXR extraction CLI.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
