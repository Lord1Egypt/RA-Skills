## Description:

A command-line agent skill for reverse engineering Android APK files with Apktool.

This skill is ready for commercial/non-commercial use.

## Publisher:

[killgfat](https://clawhub.ai/user/killgfat)

### License/Terms of Use:


## Use Case:

Developers and security engineers use this skill to get Apktool and JADX installation guidance, APK decode and rebuild commands, troubleshooting steps, and legal-use reminders for authorized Android application analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Manual install steps download executable archives and binaries before placing them on system-wide paths.

Mitigation: Prefer package-manager installation where available; when manual installation is required, verify checksums or signatures before making files executable.

Risk: Install guidance writes under /opt and /usr/local/bin, which may require elevated privileges and can affect the host system.

Mitigation: Review commands before execution and prefer user-local installation paths or isolated environments.

Risk: APK reverse engineering can create legal or policy exposure if used on apps without authorization.

Mitigation: Use the skill only for APKs the user owns or is authorized to analyze, and do not distribute modified commercial applications.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/killgfat/skills/apktool)
- [Apktool homepage](https://apktool.org)
- [Apktool documentation](https://apktool.org/docs)
- [Apktool GitHub project](https://github.com/iBotPeaches/Apktool)
- [JADX release archive referenced by install metadata](https://github.com/skylot/jadx/releases/download/v1.5.0/jadx-1.5.0.zip)
- [Install guide](references/install.md)
- [Usage guide](references/usage.md)
- [Troubleshooting guide](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown]

**Output Format:** [Markdown with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are guidance for local command-line APK analysis workflows; the skill depends on apktool, java, and jadx being available.]

## Skill Version(s):

0.0.2 (source: server release metadata and artifact documentation)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
