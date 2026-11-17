## Description:

Interactive guide for integrating MobTech FlyVerify (SecVerify) into Android projects through a five-step workflow with user confirmation at each step.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mobsupport](https://clawhub.ai/user/mobsupport)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to add MobTech FlyVerify one-click mobile authentication to Android apps, including Gradle setup, appKey/appSecret configuration, privacy consent code, verification calls, and troubleshooting guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill modifies Android project files, including Gradle configuration and application code.

Mitigation: Review the proposed diff and confirm each file change before applying it to the project.

Risk: The workflow asks for MobTech appKey and appSecret values.

Mitigation: Keep appSecret values out of tracked files and prefer an ignored local secret file, environment variable, or CI secret store.

Risk: The Gradle setup uses an external Maven repository and a dynamic FlySDK dependency.

Mitigation: Verify the Maven source and pin a specific FlySDK version before running Gradle or releasing the app.

Risk: FlyVerify behavior depends on privacy consent, MobTech review status, package/signature configuration, and supported mobile network conditions.

Mitigation: Confirm the app privacy flow, MobTech review approval, package name, signature MD5, and carrier network requirements before production release.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mobsupport/skills/andorid-flyverify-integration)
- [Mob documentation center](https://www.mob.com/wiki/list)
- [FlyVerify integration guide](https://www.mob.com/wiki/detailed?wiki=551&id=78)
- [FlyVerify SDK API documentation](https://www.mob.com/wiki/detailed?wiki=297&id=78)
- [Mob SDK compliance guide](https://www.mob.com/wiki/detailed?wiki=421&id=717)
- [FlySDK Maven repository](https://mvn.zztfly.com/android)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline Gradle, Java, properties, and shell command snippets; may generate configuration files in the target Android project.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-provided Android project path and MobTech configuration values during the workflow.]

## Skill Version(s):

2.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
