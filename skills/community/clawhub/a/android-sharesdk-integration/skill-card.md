## Description:

Interactive guide for integrating MobTech ShareSDK into Android projects with 6-step workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[haodongling](https://clawhub.ai/user/haodongling)

### License/Terms of Use:

MIT-0

## Use Case:

Android developers use this skill to integrate MobTech ShareSDK into an Android project through a confirmation-driven workflow that configures Gradle, platform credentials, privacy authorization, sharing code, and project documentation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow handles MobTech and social-platform app secrets while generating Android configuration.

Mitigation: Use placeholder or local-only credentials during agent-assisted edits, keep real secrets out of committed files and chat logs, and review generated Gradle configuration before saving.

Risk: The workflow can modify Android build files and run dependency downloads.

Mitigation: Require explicit user confirmation for file edits and Gradle execution, run in a clean branch or restricted build environment, and review diffs before building.

Risk: Mutable or poorly scoped dependency sources can change what Gradle downloads.

Mitigation: Use a pinned, verified MobSDK plugin version, prefer documented vendor repositories, and avoid the alternate legacy Maven repository unless separately verified.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/haodongling/skills/android-sharesdk-integration)
- [Mob Documentation Center](https://www.mob.com/wiki/list)
- [Mob SDK Download Center](https://www.mob.com/download)
- [Mob SDK Compliance Guide](https://www.mob.com/wiki/detailed?wiki=421&id=717)
- [Mob Maven Repository](https://mvn.mob.com/android)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Gradle, Java, shell command, Excel template, and README content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user confirmation before modifying project files or running Gradle commands.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
