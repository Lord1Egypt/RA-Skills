## Description: <br>
Android Armor Breaker helps authorized security researchers analyze protected Android APKs, bypass anti-debug protections, and extract DEX files using Frida, ADB, and root memory extraction workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[haonings](https://clawhub.ai/user/haonings) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and security researchers use this skill for authorized Android application security analysis, APK protection assessment, anti-debug testing, and DEX extraction in controlled test environments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can control rooted Android devices, bypass application protections, and read protected app memory or code. <br>
Mitigation: Use it only for authorized security research on applications you own or have written permission to analyze, and run it on a disposable emulator or dedicated test device. <br>
Risk: ADB shell commands have unsafe package-name handling according to the security evidence. <br>
Mitigation: Treat package names and APK paths as trusted input, and review or patch package-name validation before operational use. <br>
Risk: Extracted memory and DEX artifacts may contain sensitive or proprietary data. <br>
Mitigation: Keep extracted artifacts local to the controlled test environment, restrict access, and delete them when they are no longer needed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/haonings/android-armor-breaker) <br>
- [Publisher Profile](https://clawhub.ai/user/haonings) <br>
- [README](artifact/README.md) <br>
- [Security and Responsible Use Guidelines](artifact/SECURITY.md) <br>
- [Quick Start Guide](artifact/QUICK_START.md) <br>
- [Release Notes v2.2.2](artifact/RELEASE_NOTES_v2.2.2.md) <br>
- [Skill Definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and local analysis artifacts when executed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce DEX files, JSON reports, execution logs, and memory extraction artifacts on the user's authorized test device or workstation.] <br>

## Skill Version(s): <br>
2.2.6 (source: server release evidence and target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
