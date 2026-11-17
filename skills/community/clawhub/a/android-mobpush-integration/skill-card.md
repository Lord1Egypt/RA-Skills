## Description:

Guides developers through an interactive MobTech MobPush integration for Android projects, covering Gradle setup, vendor push channels, privacy authorization, message handling, aliases, and tags.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mobsupport](https://clawhub.ai/user/mobsupport)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and mobile engineers use this skill to add MobTech MobPush capabilities to Android apps. It helps configure project and app Gradle files, vendor push channels, privacy-consent callbacks, message receivers, aliases, tags, and integration documentation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow handles MobPush appSecret and vendor credentials and may write them into Gradle files or documentation.

Mitigation: Keep secrets out of README files and version-controlled Gradle files, and confirm any file write before applying it.

Risk: The workflow can add an unpinned FlySDK Gradle plugin dependency.

Mitigation: Pin and verify the FlySDK version instead of using '+'.

Risk: The workflow can run Gradle commands after changing project configuration.

Mitigation: Require explicit confirmation before every Gradle command and avoid --refresh-dependencies unless it is needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mobsupport/skills/android-mobpush-integration)
- [Mob documentation center](https://www.mob.com/wiki/list)
- [MobPush integration guide](https://www.mob.com/wiki/detailed?wiki=498&id=136)
- [Vendor channel configuration](https://www.mob.com/wiki/detailed?wiki=517&id=136)
- [Mob SDK compliance guide](https://www.mob.com/wiki/detailed?wiki=421&id=717)
- [Mob Maven repository](https://mvn.zztfly.com/android)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline code blocks, shell commands, Gradle configuration, Java snippets, XML snippets, and generated project documentation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate an Excel configuration template and project README during an interactive Android integration workflow.]

## Skill Version(s):

2.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
