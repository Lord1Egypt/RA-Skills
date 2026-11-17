## Description:

Install, configure, start, and troubleshoot ClawTime, a private self-hosted webchat UI for OpenClaw with passkey authentication, Piper TTS voice, a 3D avatar, and Cloudflare Tunnel HTTPS.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bewareofddog](https://clawhub.ai/user/bewareofddog)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to install ClawTime on a local machine, configure Cloudflare Tunnel HTTPS, register passkeys, set up optional Piper TTS, manage startup behavior, and troubleshoot OpenClaw gateway authentication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer can run mutable remote code through repository updates and npm dependency installation.

Mitigation: Review the installer before execution, use configuration values you control, and prefer a pinned reviewed ClawTime commit with audited dependencies.

Risk: Generated startup scripts and launchd persistence can preserve unsafe or unintended runtime configuration.

Mitigation: Inspect generated scripts and launchd plist files before loading them, keep tokens in macOS Keychain, and remove persistence entries that are not needed.

Risk: Token display, passkey reset, and device-key deletion are sensitive operations that can weaken access control if used casually.

Mitigation: Limit these commands to recovery or setup flows, protect setup and gateway tokens, and verify the intended ClawTime origin before registration.

Risk: The optional TTS command uses text substitution into a shell command.

Mitigation: Sanitize substituted text and prefer argument-array process execution over shell string interpolation when modifying the TTS pipeline.

## Reference(s):

- [ClawTime Setup skill page](https://clawhub.ai/bewareofddog/skills/clawtime-setup)
- [ClawTime Device Authentication Deep Dive](artifact/references/device-auth.md)
- [ClawTime launchd setup](artifact/references/launchd.md)
- [ClawTime Troubleshooting](artifact/references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command blocks and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-supplied domain, setup token, gateway token, and local toolchain state.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
