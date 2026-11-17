## Description:

Generates Android projects with Gradle configurations, optional JNI/NDK/CMake setup, and local build validation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oahc09](https://clawhub.ai/user/oahc09)

### License/Terms of Use:

MIT

## Use Case:

Developers use this skill to scaffold Android apps, choose compatible build settings, add optional native modules, and verify a debug APK through a real build.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local build checks execute Android tooling and may download build dependencies.

Mitigation: Run builds only where local command execution and dependency downloads are permitted; report scaffolding-only output if verification cannot run.

Risk: Optional device verification can replace an installed app and launch it on a connected device.

Mitigation: Disconnect devices that must not be modified or explicitly select the intended emulator or device before installation and launch.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/oahc09/skills/android-project-generator)
- [Android Gradle version compatibility matrix](references/version-matrix.md)
- [Android project configuration templates](references/config-templates.md)

## Skill Output:

**Output Type(s):** [Code, Configuration, Shell commands, Guidance]

**Output Format:** [Android project files and Markdown build-status guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports scaffolding, compilation, APK, and optional device-run verification states.]

## Skill Version(s):

1.3.1 (source: server-resolved release and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
