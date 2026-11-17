## Description:

Computer use for Windows, macOS, Linux and WSL. Screenshot the screen, list windows, click buttons by name, close/focus apps, type text, press keys, click by coordinates, and show an "agent is working" overlay. Nothing to install on Windows/macOS; Linux needs xdotool and wmctrl.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brayanjeshua](https://clawhub.ai/user/brayanjeshua)

### License/Terms of Use:

MIT

## Use Case:

Developers use this skill to let an agent inspect and operate a desktop across Windows, macOS, Linux, and WSL. It supports screenshots, window and control discovery, and targeted mouse or keyboard actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan rates the skill suspicious based on reported input controls and cancellation weaknesses, and notes that some files were only partly analyzed.

Mitigation: Before installing, review the input-lock and cancellation behavior, use input lock only for short supervised bursts, and account for the scanner's partial coverage.

## Reference(s):

- [Desktop Pilot on ClawHub](https://clawhub.ai/brayanjeshua/skills/desktop-pilot)

## Skill Output:

**Output Type(s):** [Images, Text]

**Output Format:** [PNG screenshots and plain-text window/control listings or action status messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Output depends on the selected desktop action and platform.]

## Skill Version(s):

1.0.1 (source: CHANGELOG.md, server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
