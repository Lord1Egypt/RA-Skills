## Description:

Interactive guide for integrating MobTech MobLink into Android projects with step-by-step workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mobsupport](https://clawhub.ai/user/mobsupport)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Android engineers use this skill to integrate MobTech MobLink deep linking, scene restoration, Gradle configuration, privacy authorization callbacks, and mobID generation into Android projects.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill adds an unpinned MobSDK Gradle plugin dependency.

Mitigation: Review and pin the MobSDK Gradle plugin to an approved version, and use dependency verification or locking where possible.

Risk: The integration workflow handles MobTech app secrets in plaintext project files.

Mitigation: Keep MobLink_Config.xlsx and local credential files out of version control, avoid printing appSecret in logs or diffs, delete the completed workbook after transferring configuration, and rotate any appSecret that was committed or shipped in an APK.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mobsupport/skills/android-moblink-integration)
- [MobTech MobLink Documentation Entry](https://www.mob.com/wiki/detailed?wiki=661&id=34)
- [MobTech MobLink Android Integration Guide](https://www.mob.com/wiki/detailed?wiki=115&id=34)
- [MobTech MobLink Android SDK API](https://www.mob.com/wiki/detailed?wiki=116&id=34)
- [MobTech MobLink Android Compliance Guide](https://www.mob.com/wiki/detailed?wiki=222&id=34)
- [MobTech MobLink Extended Business Function Settings](https://www.mob.com/wiki/detailed?wiki=660&id=34)
- [MobSDK Maven Repository](https://mvn.mob.com/android)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with code snippets, shell commands, Gradle configuration, and generated project files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate and read a MobLink_Config.xlsx workbook and a project-level MOBLINK_README.md during the guided integration workflow.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
