## Description:

Connect to security cameras, capture snapshots, and process video feeds with protocol support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to generate camera capture, security-system integration, and video/image processing guidance for cameras they own or administer.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Camera URLs, passwords, and bearer tokens can be exposed through command history, logs, or copied examples.

Mitigation: Use environment variables or a secret manager for credentials, avoid printing credential-bearing URLs, and review generated commands before running them.

Risk: Camera feeds and API calls may use weak transport settings or bypass certificate checks.

Mitigation: Prefer HTTPS with verified certificates, avoid curl -k with bearer tokens, and keep cameras on a protected network segment.

Risk: Snapshots and video frames may contain sensitive surveillance images, especially when sent to cloud vision services.

Mitigation: Use local processing when possible, upload only necessary images, apply retention limits, and clean up saved snapshots and clips.

Risk: Continuous monitoring can over-collect footage or poll cameras too aggressively.

Mitigation: Use the skill only with cameras the user owns or administers, prefer event-driven alerts, and limit polling frequency and retention.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivangdavila/skills/cameras)
- [Security Camera Integration](artifact/security-integration.md)
- [Webcam and USB Camera Capture](artifact/capture.md)
- [DSLR / Mirrorless Control](artifact/photography-control.md)
- [Video and Image Processing](artifact/processing.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration guidance]

**Output Format:** [Markdown guidance with inline bash, Python, JavaScript, and API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-provided camera access details; ffmpeg is required, with gphoto2 and v4l2-ctl optional for specific camera workflows.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
