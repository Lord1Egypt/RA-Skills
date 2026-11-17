## Description:

Create, build and deploy Android APKs on ARM64 Linux (DGX Spark, Raspberry Pi, ARM cloud): native aarch64 aapt2 for Gradle, plus adb install-and-verify over USB or VPN.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jagones84](https://clawhub.ai/user/jagones84)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to create, build, deploy, and verify debug Android APKs from ARM64 Linux hosts without relying on an x86-64 build machine.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Privileged package installation and Android toolchain changes can affect the host system.

Mitigation: Review package installs before execution, run setup only on intended Debian or Ubuntu ARM64 hosts, and keep Gradle overrides scoped to the target Android project.

Risk: ADB and remote ADB access can install apps or interact with a connected device if configured incorrectly.

Mitigation: Review config.sh values before running deploy scripts, keep config.sh out of version control, use the intended device serial or host, and disconnect after verification.

Risk: Copying ~/.android/adbkey exposes an Android debugging credential.

Mitigation: Prefer approving the current host on the Android device; if copying is necessary, transfer the key securely, restrict permissions, and revoke stale Android debugging authorizations afterward.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jagones84/skills/android-arm64-devkit-skill)
- [README](README.md)
- [Troubleshooting guide](docs/troubleshooting.md)
- [Examples](examples/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update Android project files, Gradle properties, local configuration, ADB state files, and verification artifacts when the referenced scripts are run.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
