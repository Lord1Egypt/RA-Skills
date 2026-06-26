## Description: <br>
Install, configure, start, and troubleshoot ClawTime, a private self-hosted OpenClaw webchat UI that uses Cloudflare Tunnel, passkeys, optional Piper TTS, and a 3D avatar. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bewareofddog](https://clawhub.ai/user/bewareofddog) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to install ClawTime, configure Cloudflare Tunnel and OpenClaw gateway access, register passkeys, enable optional Piper TTS, manage launchd startup, and diagnose common setup errors. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Mutable external application code and npm dependencies receive OpenClaw gateway credentials during setup. <br>
Mitigation: Install only when the ClawTime source and dependencies are trusted, and use a dedicated or least-privileged OpenClaw gateway token when available. <br>
Risk: Setup-token links and gateway tokens can expose access if copied into logs, scripts, shell history, or shared channels. <br>
Mitigation: Treat setup-token URLs as temporary secrets, verify the public Cloudflare URL before use, and store long-lived tokens in macOS Keychain rather than plaintext files. <br>
Risk: Optional TTS command handling can be unsafe if text substitution is not sanitized by the installed server. <br>
Mitigation: Keep TTS disabled until command handling is verified, and prefer argument-array execution over shell string interpolation when modifying the TTS pipeline. <br>
Risk: Reset commands can delete passkey credentials or device keys needed for access. <br>
Mitigation: Back up credentials or device keys before reset operations and confirm that a new device can be approved in the OpenClaw gateway. <br>


## Reference(s): <br>
- [ClawTime Device Authentication Deep Dive](artifact/references/device-auth.md) <br>
- [ClawTime Auto-Start with macOS launchd](artifact/references/launchd.md) <br>
- [ClawTime Troubleshooting](artifact/references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands, configuration snippets, and troubleshooting steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include local setup commands, environment variable guidance, Cloudflare tunnel configuration, launchd plist guidance, and reset commands for passkeys or device keys.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
