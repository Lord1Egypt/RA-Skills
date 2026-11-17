## Description:

Control a Linux X11 desktop by taking screenshots and moving/clicking/typing via xdotool + scrot.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rylena](https://clawhub.ai/user/rylena)

### License/Terms of Use:


## Use Case:

Developers and automation agents use this skill to inspect and control a trusted Linux X11 desktop session through screenshot capture, mouse actions, keyboard input, window focus, and URL opening.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can capture the visible desktop and expose private data shown in an X11 session.

Mitigation: Use it only in a trusted, isolated desktop session with credentials, private data, and unrelated applications hidden or unavailable.

Risk: The skill can type, click, focus windows, and open URLs in a real desktop session.

Mitigation: Review planned actions before use and avoid running it where destructive applications or sensitive workflows are active.

Risk: The security evidence rates the release as suspicious because desktop automation has broad control with minimal safety boundaries.

Mitigation: Review the skill carefully before installation and limit execution to environments where broad GUI control is acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rylena/skills/claw-mouse)
- [Project homepage from skill metadata](https://github.com/rylena/claw-mouse)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Text output with screenshot file paths and command-line usage]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Linux X11 with python3, xdotool, and scrot available.]

## Skill Version(s):

0.1.0 (source: server release metadata and artifact changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
