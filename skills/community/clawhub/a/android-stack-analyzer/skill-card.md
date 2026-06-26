## Description: <br>
Quickly view and analyze Android device page stacks, including the current page, Activity history, Fragments, and page-switch monitoring through ADB commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[githubzyq](https://clawhub.ai/user/githubzyq) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, QA engineers, and Android reverse-engineering practitioners use this skill to inspect foreground pages, Activity back stacks, Fragment information, recent tasks, and page switching on Android devices through ADB. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: ADB inspection commands can expose package names, page state, device properties, logs, and other sensitive debugging output. <br>
Mitigation: Use the skill only on devices you own or are authorized to debug, and redact package names, logs, and device details before sharing output. <br>
Risk: Real-time page monitoring can continuously collect foreground Activity changes while it is running. <br>
Mitigation: Run monitoring only for explicit debugging sessions and stop it when the needed observation is complete. <br>
Risk: Some dumpsys output can be incomplete, unavailable, or different across Android versions and device configurations. <br>
Mitigation: Treat results as diagnostic signals, confirm against raw dumpsys output when needed, and avoid relying on a single command for final conclusions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/githubzyq/android-stack-analyzer) <br>
- [README](artifact/README.md) <br>
- [Installation guide](artifact/INSTALL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline ADB commands and shell script examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Android SDK Platform Tools, ADB on PATH, and an authorized Android device connection.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
