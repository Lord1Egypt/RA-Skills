## Description: <br>
Guides Android developers through a confirmed, step-by-step MobTech FlyVerify (SecVerify) integration workflow covering configuration, Gradle setup, privacy authorization, pre-verification, one-click login, and troubleshooting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mobsupport](https://clawhub.ai/user/mobsupport) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to integrate MobTech FlyVerify one-click phone verification into Android projects. It helps gather project configuration, propose Android and Gradle changes, add privacy authorization and login code, and produce project-level integration guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill proposes Android project-file edits that can change build behavior. <br>
Mitigation: Use it only in a version-controlled project or backup branch, and review each proposed file change before approval. <br>
Risk: The workflow handles MobTech appKey and appSecret values during configuration. <br>
Mitigation: Keep appKey and appSecret private, avoid committing generated configuration files with secrets, and verify where credentials are inserted. <br>
Risk: The integration adds a Maven repository, FlyVerify dependency configuration, and may run Gradle dependency refresh commands. <br>
Mitigation: Verify the Maven repository and FlyVerify dependency source before approving changes, and run Gradle only after reviewing the dependency resolution impact. <br>


## Reference(s): <br>
- [Mob documentation center](https://www.mob.com/wiki/list) <br>
- [FlyVerify integration guide](https://www.mob.com/wiki/detailed?wiki=551&id=78) <br>
- [FlyVerify SDK API documentation](https://www.mob.com/wiki/detailed?wiki=297&id=78) <br>
- [Mob SDK compliance guide](https://www.mob.com/wiki/detailed?wiki=421&id=717) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline code, shell commands, configuration snippets, and generated project files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose edits to Android project files and generate an Excel configuration template and integration README after user confirmation.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
