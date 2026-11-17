## Description:

Execute Android ADB (Android Debug Bridge) commands for device management, app management, debugging, and automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cwener](https://clawhub.ai/user/cwener)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to manage, inspect, debug, and automate connected Android devices through ADB commands while preserving device selection and command-safety guardrails.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives an agent broad ADB control over connected Android devices, including operations that can change apps, data, settings, or device state.

Mitigation: Require explicit device selection for multi-device sessions, preview risky commands, and obtain clear confirmation before destructive ADB operations.

Risk: Some logcat helper and terminal-launch behavior can turn user-supplied filters or command fragments into host shell commands.

Mitigation: Avoid untrusted filters, pass command arguments without eval or bash-c interpolation, and review or fix the helper scripts before installation.

Risk: The bundled installer downloads Android platform tools without checksum verification.

Mitigation: Prefer an already installed trusted ADB binary, or add checksum verification before using the local installer.

Risk: Logs, screenshots, recordings, UI dumps, and pulled files can contain sensitive device, user, or application data.

Mitigation: Treat generated files as sensitive, write them only to intentional locations, and redact sensitive content before sharing.

## Reference(s):

- [ADB Command Reference](references/adb-commands.md)
- [ClawHub Skill Page](https://clawhub.ai/cwener/skills/android-adb-2)
- [ClawHub Publisher Profile](https://clawhub.ai/user/cwener)
- [Android Platform Tools for Linux](https://dl.google.com/android/repository/platform-tools-latest-linux.zip)
- [Android Platform Tools for macOS](https://dl.google.com/android/repository/platform-tools-latest-darwin.zip)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and concise command-output summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May run or propose ADB commands, helper scripts, and local file outputs such as logs or screenshots when requested.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
