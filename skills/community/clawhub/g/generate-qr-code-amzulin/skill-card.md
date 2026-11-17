## Description:

Generates QR code images from text, URLs, or WiFi information, with configurable size, color, and save location.

This skill is ready for commercial/non-commercial use.

## Publisher:

[amzulin](https://clawhub.ai/user/amzulin)

### License/Terms of Use:


## Use Case:

End users and agents use this skill to convert supplied text, URLs, phone numbers, or WiFi credentials into scannable QR code image files. It is useful when a conversation needs to produce a local QR image and report the saved path or a clear error message.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically install Python packages and modify the active Python environment.

Mitigation: Review before installation, run in a managed or isolated environment, and prefer pinned dependency installation performed explicitly by the operator.

Risk: QR images may persist sensitive payloads, including WiFi credentials, on disk.

Mitigation: Confirm the save location before generating sensitive QR codes, restrict file access to trusted users, and remove generated images when they are no longer needed.

Risk: The skill writes image files to a default or user-supplied path.

Mitigation: Use an intended output directory with appropriate permissions and avoid paths that expose files to shared or untrusted locations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/amzulin/skills/generate-qr-code-amzulin)
- [Publisher profile](https://clawhub.ai/user/amzulin)

## Skill Output:

**Output Type(s):** [Text, Files]

**Output Format:** [PNG image file plus a text status or error message]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes the generated QR image to the requested path, or to a desktop qr_code.png file when no path is supplied.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
