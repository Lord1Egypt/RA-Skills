## Description:

Creates QR code images containing text, URLs, or WiFi details, with configurable size, color, and save path.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lanxianghua](https://clawhub.ai/user/lanxianghua)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill when a user asks to convert text, URLs, or WiFi details into a QR code image and save it to a specified path or the desktop by default.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill automatically installs unpinned Python packages.

Mitigation: Use an isolated or managed Python environment and preinstall reviewed dependencies before enabling the skill.

Risk: The skill can write to a user-selected save path and may overwrite an existing writable file.

Mitigation: Review requested save locations before execution and avoid letting untrusted instructions choose output paths.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Files]

**Output Format:** [Plain text status response plus a PNG image file written to disk]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The output path is user-controllable and may create directories or replace an existing writable file.]

## Skill Version(s):

1.0.0 (source: release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
