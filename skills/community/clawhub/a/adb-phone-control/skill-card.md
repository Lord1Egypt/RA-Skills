## Description:

Use when the user asks to control, operate, or automate an Android phone via ADB — tapping, swiping, typing, launching apps, or any UI interaction on a connected device.

This skill is ready for commercial/non-commercial use.

## Publisher:

[txmonkey](https://clawhub.ai/user/txmonkey)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to control and automate a connected Android device through ADB using a structured observe-locate-act-verify loop.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can operate a real Android device through ADB.

Mitigation: Use it only with devices and apps where the operator has authorization, and verify each action before continuing.

Risk: Screenshots and UI dumps may capture sensitive on-screen information and leave files on disk.

Mitigation: Set ADB_OUTPUT_DIR to a private directory and avoid using the skill on personal, financial, messaging, or production apps.

Risk: The recursive explorer can broadly crawl an app and trigger unintended navigation or actions.

Mitigation: Limit exploration depth, review target apps before crawling, and avoid recursive exploration on sensitive or production applications.

Risk: Evidence reports unsafe input and path handling.

Mitigation: Do not pass untrusted text or untrusted environment values to the helpers until those issues are fixed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/txmonkey/skills/adb-phone-control)

## Skill Output:

**Output Type(s):** [Shell commands, Markdown, Code, Configuration]

**Output Format:** [Markdown guidance with inline shell commands; helper scripts can generate screenshots, UI XML dumps, JSON crawl trees, and Markdown crawl summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires adb and python3; screenshots and UI dumps are written to ADB_OUTPUT_DIR or the default temporary output path.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
