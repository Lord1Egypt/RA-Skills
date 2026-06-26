## Description: <br>
Interactive guide for integrating MobTech ShareSDK into Android projects through a six-step workflow with user confirmation before project changes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[haodongling](https://clawhub.ai/user/haodongling) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to integrate MobTech ShareSDK into Android apps, including Gradle setup, platform devInfo configuration, privacy consent callbacks, share code insertion, and project documentation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can propose and apply edits to Android project files, including Gradle configuration, privacy callbacks, and sharing code. <br>
Mitigation: Use a git branch, review diffs before applying changes, and approve Gradle sync only for a trusted project. <br>
Risk: The integration workflow handles MobTech app keys, app secrets, and platform credentials. <br>
Mitigation: Do not paste live secrets into chat, and keep generated credential files out of public repositories. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/haodongling/android-sharesdk-integration) <br>
- [Mob documentation center](https://www.mob.com/wiki/list) <br>
- [Mob SDK download center](https://www.mob.com/download) <br>
- [Mob SDK compliance guide](https://www.mob.com/wiki/detailed?wiki=421&id=717) <br>
- [Mob Android Maven repository](https://mvn.mob.com/android) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with code blocks, shell commands, configuration snippets, and generated project files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate an Excel configuration template and SHARESDK_README.md in the user's Android project after confirmation.] <br>

## Skill Version(s): <br>
2.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
