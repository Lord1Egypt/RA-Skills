## Description:

Create product demo videos by automating browser interactions, capturing browser frames with Playwright CDP screencast, and encoding them with FFmpeg.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xs4m1337](https://clawhub.ai/user/0xs4m1337)

### License/Terms of Use:


## Use Case:

Developers and product teams use this skill to plan and record browser-based product walkthroughs, then encode captured frames into MP4, GIF, or WebM demos.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recorded demos can capture sensitive on-screen data from the controlled browser session.

Mitigation: Use demo accounts or sanitized data and review captured frames before sharing.

Risk: The recorder removes and recreates the configured frame output directory before saving frames.

Mitigation: Point the output directory at a disposable demo folder and verify the path before recording.

## Reference(s):

- [Demo Planning Guide](references/demo-planning.md)
- [Demo Video Creator on ClawHub](https://clawhub.ai/0xs4m1337/skills/demo-video)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with JavaScript and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The provided scripts can produce captured JPEG frame files and encoded MP4, GIF, or WebM assets when run in a configured browser and FFmpeg environment.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
