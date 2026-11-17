## Description:

AI-powered Android phone control for opening apps, tapping, typing, taking screenshots, and running phone tasks through ADB and DroidRun.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harshilmathur](https://clawhub.ai/user/harshilmathur)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to let an agent control a dedicated Android test device over USB or TCP/WiFi for mobile app interaction, screenshots, setup tasks, and scripted phone workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can give an agent broad control over an Android device, including apps, messages, purchases, account changes, and other sensitive actions.

Mitigation: Use a dedicated device that you own, keep personal accounts and sensitive apps off the device, and require explicit human review before purchases, messages, rides, banking, or account changes.

Risk: Screenshots and visible screen text may be sent to the configured vision model provider during task execution.

Mitigation: Run the skill only on a test device with no private messages, medical data, 2FA codes, banking screens, saved secrets, or other sensitive content visible.

Risk: ANDROID_PIN handling is called out by security guidance as under-disclosed and not yet safe for routine use.

Mitigation: Do not set ANDROID_PIN until PIN redaction is fixed; unlock the device manually or use the no-unlock path when practical.

Risk: ADB over TCP/WiFi can expose device-control access on the network.

Mitigation: Prefer USB for routine use, or use an SSH tunnel on untrusted networks.

## Reference(s):

- [Android Agent on ClawHub](https://clawhub.ai/harshilmathur/skills/android-agent)
- [DroidRun](https://github.com/droidrun/droidrun)
- [DroidRun releases](https://github.com/droidrun/droidrun/releases)
- [Android SDK Platform Tools](https://developer.android.com/tools/releases/platform-tools)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with command-line examples and runtime text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ADB, DroidRun, an OpenAI API key, and an authorized Android device.]

## Skill Version(s):

1.1.1 (source: server release metadata and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
