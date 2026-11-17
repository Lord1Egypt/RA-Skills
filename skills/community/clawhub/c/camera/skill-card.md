## Description:

Capture photos from MacBook webcams. Use when user asks to take a photo, picture, snapshot, or see them. Two cameras available - Brio (front-facing on monitor) and FaceTime (side angle from MacBook).

This skill is ready for commercial/non-commercial use.

## Publisher:

[therohitdas](https://clawhub.ai/user/therohitdas)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to have an agent capture webcam snapshots from configured MacBook cameras with ffmpeg commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can activate webcams and capture privacy-sensitive images or short warmup videos.

Mitigation: Use only after explicit user intent and require confirmation before activating a camera.

Risk: Captured photos and warmup videos are written to predictable /tmp paths.

Mitigation: Use private per-run temporary directories where possible and delete warmup videos after capture.

Risk: Other camera applications can conflict with capture commands.

Mitigation: Close other camera applications before running capture commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/therohitdas/skills/camera)

## Skill Output:

**Output Type(s):** [Shell commands, Files, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces JPEG photo files in /tmp and temporary warmup videos that can be deleted.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
