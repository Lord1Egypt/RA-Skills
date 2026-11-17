## Description:

Control the local computer's built-in camera for capturing photos and basic operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dddjj0](https://clawhub.ai/user/dddjj0)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill when a user explicitly asks to list local cameras, preview the webcam, or capture a photo and return the saved image path.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can open the local webcam, preview camera input, and capture images without an embedded just-in-time consent requirement.

Mitigation: Require clear user confirmation before each capture or preview request, and avoid treating ambiguous prompts as consent.

Risk: The skill depends on OpenCV for camera access.

Mitigation: Review or pin the OpenCV dependency before installation in managed environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dddjj0/skills/camera-capture)
- [ClawHub publisher profile](https://clawhub.ai/user/dddjj0)

## Skill Output:

**Output Type(s):** [Text, Files, Shell commands]

**Output Format:** [Plain text path with JPEG image file output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Captured photos are saved to the configured output path or the default captures directory.]

## Skill Version(s):

1.0.2 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
