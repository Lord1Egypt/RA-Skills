## Description: <br>
Interactive guide for integrating MobTech MobPush into Android projects with a confirmation-driven workflow for Gradle setup, vendor push channels, message handling, and privacy-compliance callbacks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mobsupport](https://clawhub.ai/user/mobsupport) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to add MobTech MobPush to Android applications, including SDK configuration, vendor channel setup, privacy authorization callbacks, and troubleshooting guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: MobPush appKey, appSecret, and vendor-channel credentials may be written to generated configuration or documentation files and displayed in chat output. <br>
Mitigation: Keep generated files containing credentials out of version control, move secrets to ignored local properties or a secret manager, and avoid pasting sensitive values into shared logs or transcripts. <br>
Risk: The skill can propose Android project file edits and Gradle dependency commands that affect builds and dependency resolution. <br>
Mitigation: Run it on a disposable branch, review each proposed file change before approval, and require explicit confirmation before Gradle commands are executed. <br>


## Reference(s): <br>
- [Android Mobpush Integration on ClawHub](https://clawhub.ai/mobsupport/android-mobpush-integration) <br>
- [Mob Documentation Center](https://www.mob.com/wiki/list) <br>
- [MobPush Integration Guide](https://www.mob.com/wiki/detailed?wiki=498&id=136) <br>
- [MobPush Vendor Channel Configuration](https://www.mob.com/wiki/detailed?wiki=517&id=136) <br>
- [Mob SDK Compliance Guide](https://www.mob.com/wiki/detailed?wiki=421&id=717) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with Gradle, Java, XML, properties, and shell code blocks; may also create Excel and Markdown project files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requests user confirmation before project file edits and Gradle commands.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
