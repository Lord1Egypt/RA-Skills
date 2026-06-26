## Description: <br>
Generate Android projects that compile on the first real build, including optional JNI/NDK/CMake native setup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oahc09](https://clawhub.ai/user/oahc09) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to create, configure, and verify Android projects with Gradle, Kotlin DSL, Android SDK tooling, and optional JNI/NDK/CMake native modules. It is intended for new project generation, version compatibility checks, environment audits, and real assembleDebug validation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run local Android build tools and Gradle commands that may download dependencies. <br>
Mitigation: Use it in an approved workspace or sandbox, review generated Gradle files and wrappers before building untrusted projects, and allow network access only when dependency resolution is expected. <br>
Risk: Optional adb verification can install and launch a generated debug APK on a connected device or emulator. <br>
Mitigation: Prefer a disposable emulator for runnable verification and confirm the target device before adb install or launch commands are run. <br>
Risk: Generated reports may be opened in a browser context where third-party CDN loading could be sensitive. <br>
Mitigation: Open generated HTML reports only in a non-sensitive browser context when external asset loading is a concern. <br>
Risk: Android build claims can be misleading if the local JDK, SDK, Gradle, wrapper, or platform versions are incomplete or mismatched. <br>
Mitigation: Run the environment audit first, resolve blocking issues, and report a project as compiled only after assembleDebug succeeds and the debug APK is confirmed. <br>


## Reference(s): <br>
- [Configuration Templates](references/config-templates.md) <br>
- [Android Gradle Version Compatibility Matrix](references/version-matrix.md) <br>
- [Reporting Guide](docs/REPORTING.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/oahc09/android-project-generator) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and generated Android project files/configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Gradle, Kotlin DSL, Android manifest, resource, wrapper, local.properties, test-report, and validation-status outputs depending on the requested workflow.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
