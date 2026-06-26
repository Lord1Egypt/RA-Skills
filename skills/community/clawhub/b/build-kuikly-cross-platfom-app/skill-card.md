## Description: <br>
Creates, builds, previews, and helps repair cross-platform mobile apps using Kuikly and the create-kuikly-app CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wwwcg](https://clawhub.ai/user/wwwcg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to scaffold Kuikly Kotlin Multiplatform mobile apps, add pages or components, run Android and iOS builds, preview on devices or simulators, and apply scoped source fixes after build diagnostics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The server security review marks the release suspicious because it includes an unrelated GitHub account action. <br>
Mitigation: Install only after reviewing that behavior, and do not approve any GitHub star action unless you intentionally want your GitHub account to star the repository. <br>
Risk: The skill can download the KuiklyUI reference repository and invoke local mobile build, package, device, and simulator tools. <br>
Mitigation: Run it in a trusted project workspace with the expected Node, JDK 17, Android SDK, Xcode, CocoaPods, adb, and simulator tooling installed, and review proposed commands before execution. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/wwwcg/build-kuikly-cross-platfom-app) <br>
- [create-kuikly-app](https://github.com/wwwcg/create-kuikly-app) <br>
- [KuiklyUI Reference Repository](https://github.com/Tencent-TDS/KuiklyUI) <br>
- [Kuikly Compose DSL Guide](references/kuiklyComposeDSL.md) <br>
- [Kuikly DSL Guide](references/kuiklyDSL.md) <br>
- [UI Framework Guide](references/ui-framework-guide.md) <br>
- [Component API Guide](references/component-api-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Kotlin code snippets, shell commands, and structured JSON command output interpretation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce or modify project files within a generated Kuikly app workspace when the user asks it to build or repair an app.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
