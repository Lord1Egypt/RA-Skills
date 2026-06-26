## Description: <br>
(macOS) Discord voice assistant installer. Install/update discord-local-stt-tts (Discord voice, Discord local, local STT + local TTS) from GitHub Releases. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vilmire](https://clawhub.ai/user/vilmire) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw users use this macOS-only skill to install or update the discord-local-stt-tts plugin for Discord voice workflows with local STT and local TTS. It downloads the latest upstream GitHub Release, installs it into the OpenClaw plugin directory, and leaves plugin enablement/configuration to the user. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The installer downloads and optionally builds the current upstream GitHub Release and its dependencies. <br>
Mitigation: Install only if the upstream `vilmire/discord-local-stt-tts` project is trusted; review the release and package scripts first, or run dependency and build steps manually in a controlled environment. <br>
Risk: Apple Speech and microphone permissions may be needed for local STT workflows. <br>
Mitigation: Grant macOS Speech Recognition and Microphone permissions only when required for the chosen STT configuration, and review plugin settings before enabling it in OpenClaw. <br>


## Reference(s): <br>
- [discord-local-stt-tts plugin repository](https://github.com/vilmire/discord-local-stt-tts) <br>
- [ClawHub skill page](https://clawhub.ai/vilmire/discord-local-stt-tts-installer) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [macOS-only installer guidance; the skill does not modify openclaw.json.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
