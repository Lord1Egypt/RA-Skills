## Description:

Controls Android devices via ADB, including UI layout analysis with uiautomator, screenshots with screencap, app launches, text input, taps, key events, swipes, and command sequences.

This skill is ready for commercial/non-commercial use.

## Publisher:

[staticai](https://clawhub.ai/user/staticai)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to connect to Android devices over USB or wireless debugging, inspect UI state, automate app interactions, and verify device state through screenshots.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ADB commands can affect apps, accounts, and device state through taps, text entry, key events, screenshots, and wireless connections.

Mitigation: Review commands before execution, confirm the intended target with adb devices, and use the skill only with devices and accounts you intend the agent to operate.

Risk: Wireless debugging can connect an Android device to an unintended host or network if pairing and connection details are mishandled.

Mitigation: Use the pairing code and connection port shown on the device, verify the connection before automation, and disable wireless debugging when finished.

## Reference(s):


## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline ADB shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include commands that operate on connected Android devices.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
