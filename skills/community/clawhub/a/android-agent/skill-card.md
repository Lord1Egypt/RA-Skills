## Description: <br>
Controls a real Android phone through ADB and DroidRun so an AI agent can inspect the screen, tap, type, swipe, run tasks, and capture screenshots. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[harshilmathur](https://clawhub.ai/user/harshilmathur) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and automation operators use this skill to connect an Android test device over USB or TCP/WiFi, verify device status, and run natural-language mobile tasks through a vision-enabled AI agent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an AI agent broad control over an unlocked Android device and sensitive apps. <br>
Mitigation: Install it only for a spare or test Android device, avoid personal banking, MFA, medical, email, and private messaging accounts, and disable ADB debugging plus DroidRun Accessibility permissions when finished. <br>
Risk: The agent may initiate purchases, messages, calls, or account changes while completing a task. <br>
Mitigation: Manually confirm purchases, messages, calls, and account changes before allowing them to proceed. <br>
Risk: Using a real phone PIN in the environment can expose credentials to the host environment. <br>
Mitigation: Do not use a real phone PIN in the environment; prefer a disposable test-device PIN or manual unlock. <br>
Risk: WiFi ADB can expose device control over the network. <br>
Mitigation: Prefer USB or an SSH tunnel over WiFi ADB, especially on untrusted networks. <br>


## Reference(s): <br>
- [ClawHub android-agent release page](https://clawhub.ai/harshilmathur/android-agent) <br>
- [Publisher profile](https://clawhub.ai/user/harshilmathur) <br>
- [DroidRun project](https://github.com/droidrun/droidrun) <br>
- [DroidRun releases](https://github.com/droidrun/droidrun/releases) <br>
- [Android SDK Platform Tools](https://developer.android.com/tools/releases/platform-tools) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown guidance with bash commands; scripts emit terminal status text and can save PNG screenshots.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ADB, Python dependencies, an OpenAI API key, and a connected Android device with appropriate debugging and accessibility permissions.] <br>

## Skill Version(s): <br>
1.1.1 (source: server-resolved release metadata and artifact/skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
