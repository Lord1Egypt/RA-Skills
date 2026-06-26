## Description: <br>
Interactive guide for integrating MobTech MobLink into Android projects with step-by-step workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mobsupport](https://clawhub.ai/user/mobsupport) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to integrate MobTech MobLink into Android applications, including Gradle setup, MobLink configuration, privacy authorization handling, scene restoration, and mobID generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow may propose edits to Android Gradle files, privacy authorization callbacks, and scene restoration code. <br>
Mitigation: Review proposed changes and confirm diffs before applying them to an Android project. <br>
Risk: The workflow handles MobTech appKey and appSecret values supplied by the user. <br>
Mitigation: Keep credentials scoped to authorized projects and avoid publishing generated files or logs that expose secrets. <br>
Risk: The artifact includes a helper script that generates an Excel configuration template. <br>
Mitigation: Run the script only in a trusted ClawHub development or maintainer environment and review commands before execution. <br>


## Reference(s): <br>
- [MobLink Documentation Entry](https://www.mob.com/wiki/detailed?wiki=661&id=34) <br>
- [MobLink Android Integration Guide](https://www.mob.com/wiki/detailed?wiki=115&id=34) <br>
- [MobLink Android SDK API](https://www.mob.com/wiki/detailed?wiki=116&id=34) <br>
- [MobLink Android Compliance Guide](https://www.mob.com/wiki/detailed?wiki=222&id=34) <br>
- [MobLink Extended Business Function Settings](https://www.mob.com/wiki/detailed?wiki=660&id=34) <br>
- [MobSDK Android Maven Repository](https://mvn.mob.com/android) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown with inline code blocks, configuration snippets, shell commands, and generated project files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce an Excel configuration template and a MobLink integration README for the target Android project.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
