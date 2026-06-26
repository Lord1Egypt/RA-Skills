## Description: <br>
Use when the user asks to control, operate, or automate an Android phone via ADB, including tapping, swiping, typing, launching apps, or other UI interaction on a connected device. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[txmonkey](https://clawhub.ai/user/txmonkey) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation agents use this skill to operate a connected Android device through ADB with an observe-locate-act-verify loop. It supports UI hierarchy inspection, screenshots, taps, swipes, text entry, app launch, and bounded app exploration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can perform real actions on a connected Android device through ADB, including taps, swipes, text input, app launches, and recursive exploration. <br>
Mitigation: Use it only with explicit user intent, verify each step before continuing, and avoid recursive exploration in apps where automated taps could cause account, financial, messaging, or data-changing side effects. <br>
Risk: Screenshots, UI dumps, and clipboard/text input can expose sensitive on-device content. <br>
Mitigation: Use a private ADB_OUTPUT_DIR, avoid sensitive screens, and delete screenshots and UI dumps when the task is complete. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/txmonkey/adb-phone-control) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Code, Configuration, Guidance, JSON, Markdown] <br>
**Output Format:** [Markdown guidance with bash commands; helper scripts can produce screenshots, UI dumps, JSON trees, and Markdown exploration reports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires adb and python3; may write screenshots and UI dumps to ADB_OUTPUT_DIR or /tmp.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
