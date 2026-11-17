## Description:

Guides developers through integrating MobTech SMSSDK SMS verification into Android projects, including configuration, Gradle setup, privacy consent, and verification-code code paths.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mobsupport](https://clawhub.ai/user/mobsupport)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to add MobTech SMSSDK SMS verification to Android apps through an interactive, confirmation-based workflow. It helps with project validation, configuration collection, SDK setup, privacy authorization, built-in or custom UI integration, and troubleshooting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow collects MobTech AppKey and AppSecret values and may place them in a project-root spreadsheet.

Mitigation: Keep the spreadsheet out of version control, remove it when no longer needed, and avoid committing credentials or generated configuration containing secrets.

Risk: The workflow edits Android project files and proposes running Gradle commands in a user-provided project path.

Mitigation: Review each proposed file change before applying it and run Gradle manually from a trusted project directory.

Risk: The Gradle plugin example uses an unpinned MobSDK dependency version.

Mitigation: Pin the MobSDK Gradle plugin to a reviewed version before production use.

Risk: SMSSDK integration requires privacy-consent handling before SDK initialization.

Mitigation: Confirm the app presents a privacy policy and calls the MobSDK privacy authorization method only after user consent.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mobsupport/skills/android-smssdk-integration)
- [Mob documentation center](https://www.mob.com/wiki/list)
- [MobTech SMSSDK product overview](https://mob.com/wiki/detailed?wiki=163&id=23)
- [SMSSDK integration guide and API reference](https://mob.com/wiki/detailed?wiki=440&id=23)
- [MobSDK privacy compliance guide](https://mob.com/wiki/detailed?wiki=210&id=23)
- [SMSSDK server-side verification API](https://mob.com/wiki/detailed?wiki=112&id=23)
- [SMSSDK SMS settings](https://mob.com/wiki/detailed?wiki=452&id=23)
- [SMSSDK FAQ](https://mob.com/wiki/detailed?wiki=123&id=23)
- [SMS signature rules update](https://mob.com/wiki/detailed?wiki=732&id=23)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Gradle snippets, Java code blocks, shell commands, and configuration-file instructions.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate an Excel configuration template and project README in the target Android project when the user confirms the workflow steps.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
