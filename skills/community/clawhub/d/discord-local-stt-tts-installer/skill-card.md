## Description:

(macOS) Discord voice assistant installer. Install/update discord-local-stt-tts (Discord voice, Discord local, local STT + local TTS) from GitHub Releases.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vilmire](https://clawhub.ai/user/vilmire)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw users on macOS use this skill to install or update the discord-local-stt-tts plugin for local speech-to-text and text-to-speech in Discord voice workflows. Users still need to restart OpenClaw and enable or configure the plugin separately.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer downloads mutable latest-release source from GitHub without a pinned checksum.

Mitigation: Install only from a trusted upstream release, or inspect and pin a checksummed artifact before running the installer.

Risk: If pnpm is available, local dependency installation and build scripts may run under the user's account.

Mitigation: Review the downloaded source and dependencies before allowing the optional build step, and run the installer in a trusted user environment.

Risk: The Discord voice workflow may require local microphone and speech recognition permissions on macOS.

Mitigation: Grant only the permissions needed for the chosen local STT engine and review macOS privacy settings before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vilmire/skills/discord-local-stt-tts-installer)
- [discord-local-stt-tts plugin repository](https://github.com/vilmire/discord-local-stt-tts)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [macOS-only installer guidance; may include OpenClaw restart, plugin configuration, ffmpeg, and macOS microphone or speech recognition permission notes.]

## Skill Version(s):

0.1.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
