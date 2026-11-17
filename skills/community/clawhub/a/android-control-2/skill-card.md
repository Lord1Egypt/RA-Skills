## Description:

Control an Android device via command-line tools (uiautomator, screencap, input, am). Automatically attempts non-root execution first and falls back to root if necessary.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kv0768](https://clawhub.ai/user/kv0768)

### License/Terms of Use:


## Use Case:

Developers and device operators use this skill to inspect and control an Android device from an agent session by collecting UI snapshots, capturing screenshots, simulating touch and text input, and launching apps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can retry screenshots, UI dumps, taps, swipes, app launches, and text entry with already-authorized root access when normal Android commands fail.

Mitigation: Install only when agent-controlled Android device operation is intended; remove automatic su fallbacks or require explicit confirmation before elevated actions.

Risk: Screenshots and UI hierarchy dumps can expose visible sensitive data from the device.

Mitigation: Avoid using the skill while credentials, private messages, financial apps, or other sensitive content are visible.

## Reference(s):

- [Android UI Automator documentation](https://developer.android.com/studio/test/uiautomator)
- [ClawHub Android Control skill page](https://clawhub.ai/kv0768/skills/android-control-2)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include commands that collect UI hierarchy XML, base64-encoded screenshots, or perform device input actions.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
