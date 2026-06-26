## Description: <br>
Control an Android device via command-line tools (uiautomator, screencap, input, am), trying non-root execution first and falling back to root when available. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kv0768](https://clawhub.ai/user/kv0768) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and device automation operators use this skill to inspect and control an Android device from an agent session with Android command-line tools, including UI dumps, screenshots, taps, swipes, app launches, and text input. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can retry Android commands through root access when non-root execution fails. <br>
Mitigation: Use it only on a device where root-backed control is intended, and require explicit confirmation before any root-backed action. <br>
Risk: Screenshots and UI hierarchy captures can expose sensitive screen data. <br>
Mitigation: Prefer a test device, keep sensitive screens closed, and confirm before captures are taken. <br>
Risk: Input, launch, and settings actions can change device state or trigger user-facing actions. <br>
Mitigation: Require explicit confirmation before text entry, settings changes, purchases, messages, or other state-changing operations. <br>


## Reference(s): <br>
- [Android UI Automator documentation](https://developer.android.com/studio/test/uiautomator) <br>
- [ClawHub release page](https://clawhub.ai/kv0768/android-control-2) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown instructions with inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include commands for UI hierarchy XML, screenshot data, input events, app launches, and text entry.] <br>

## Skill Version(s): <br>
0.1.1 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
