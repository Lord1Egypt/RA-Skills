## Description:

Install Android Lab's local Docker images, then build an Android app, boot a private emulator, install APKs and inspect the UI from the app's own directory. Use when an Android build or emulator is needed without a host SDK or ADB.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psyb0t](https://clawhub.ai/user/psyb0t)

### License/Terms of Use:

MIT-0

## Use Case:

Android developers use this skill to build applications and operate a private Docker-based emulator for installing apps and inspecting their UI, without a host Android SDK or ADB.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Emulator helper containers have broad control over the Docker host.

Mitigation: Use a dedicated VM without sensitive host mounts, and review the selected release's installer and container code before using emulator commands.

Risk: The .android-lab directory contains signing material and saved device data.

Mitigation: Keep .android-lab out of Git.

## Reference(s):

- [Android Lab commands](artifact/references/setup.md)
- [Android Lab project homepage](https://github.com/psyb0t/android-lab)
- [Android Lab on ClawHub](https://clawhub.ai/psyb0t/skills/android-lab)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance, Files]

**Output Format:** [Markdown guidance with shell commands; Android build and emulator artifacts such as APK, JSON, XML, and PNG files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Build outputs and emulator inspection files are written in the Android project.]

## Skill Version(s):

0.16.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
