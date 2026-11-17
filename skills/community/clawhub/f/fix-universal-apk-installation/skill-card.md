## Description:

Helps agents guide developers through repairing universal_signed.apk installation failures on Android 11+ by updating APK manifest handling, resource compression, alignment, and signing steps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[softwareme](https://clawhub.ai/user/softwareme)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and mobile engineers use this skill when a merged universal APK fails to install because native libraries cannot be extracted or resources.arsc is compressed or misaligned. It provides procedural guidance and shell-command examples for unpacking, modifying, rebuilding, aligning, signing, and checking the APK.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill rewrites and signs APK files, which can alter package integrity and installation behavior.

Mitigation: Keep a backup of the original APK, test on a disposable device or emulator, and verify the package name and signing certificate before installation.

Risk: The artifact uses hard-coded local paths and signing material examples that may be inappropriate for another environment.

Mitigation: Replace paths and signing credentials with environment-specific values and protect keystores and passwords outside shared scripts.

Risk: Sideloading repaired APKs can expose devices to untrusted application risk.

Mitigation: Install only APKs from trusted sources, disable unknown-source installation after testing, and follow the security guidance from the release evidence.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/softwareme/skills/fix-universal-apk-installation)
- [Publisher profile](https://clawhub.ai/user/softwareme)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include APK toolchain commands, signing guidance, Android SDK build-tools paths, and verification steps.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
