## Description:

Control desktop applications across Windows, WSL, macOS, and Linux with screenshots, accessibility-based clicks, window focus, typing, and keyboard input.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brayanjeshua](https://clawhub.ai/user/brayanjeshua)

### License/Terms of Use:

MIT No Attribution (MIT-0)

## Use Case:

Developers and agent builders use this skill to inspect and operate desktop applications during supervised GUI workflows, including screenshots, selecting controls, typing, and keyboard or mouse actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan marks this release suspicious because of environment-related concerns and incomplete inspection of several components; the available evidence does not establish that it is safe.

Mitigation: Review the release carefully before installation, especially the components that were not fully inspected.

Risk: Screenshots can capture private windows or notifications, and the optional Windows input lock suppresses physical keyboard and mouse input while active.

Mitigation: Keep screenshots local and remove them when no longer needed; use input lock only for short, supervised bursts.

## Reference(s):

- [Desktop Pilot release on ClawHub](https://clawhub.ai/brayanjeshua/skills/desktop-pilot)

## Skill Output:

**Output Type(s):** [Text, Images]

**Output Format:** [Command-line status and accessibility text, plus PNG screenshots]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Screenshots may contain private desktop content.]

## Skill Version(s):

1.0.3 (source: CHANGELOG and server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
