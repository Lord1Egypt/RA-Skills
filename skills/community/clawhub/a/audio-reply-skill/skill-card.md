## Description: <br>
Generate audio replies using TTS. Trigger with "read it to me [public URL]" to fetch and read content aloud, or "talk to me [topic]" to generate a spoken response. Also responds to "speak", "say it", "voice reply". <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MaTriXy](https://clawhub.ai/user/MaTriXy) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and Claude Code users use this skill to turn concise assistant responses or public web content summaries into local spoken audio replies on Apple Silicon Macs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad trigger phrases such as "speak" or "say it" may start local audio playback unexpectedly. <br>
Mitigation: Confirm the user's intent before running TTS when a trigger is ambiguous, and keep playback local with normal device volume controls. <br>
Risk: URL reading can expose private, authenticated, or sensitive content to TTS processing and chat history. <br>
Mitigation: Process only public, non-sensitive HTTP(S) URLs; reject local, private, authenticated, signed, or secret-bearing links; ask for redacted pasted text when needed. <br>
Risk: First use may download the TTS model and dependencies through uv and then run local playback commands. <br>
Mitigation: Install uv from a trusted source, verify it is on PATH, and review the generated command before execution. <br>
Risk: Generated temporary audio files may retain spoken content if cleanup fails. <br>
Mitigation: Use unique temporary file prefixes and delete generated WAV files after playback. <br>


## Reference(s): <br>
- [ClawHub Audio Reply release page](https://clawhub.ai/MaTriXy/audio-reply-skill) <br>
- [MLX Audio](https://github.com/Blaizzy/mlx-audio) <br>
- [chatterbox-turbo-fp16 model](https://huggingface.co/mlx-community/chatterbox-turbo-fp16) <br>
- [uv package manager](https://github.com/astral-sh/uv) <br>
- [MLX framework](https://github.com/ml-explore/mlx) <br>


## Skill Output: <br>
**Output Type(s):** [audio, text, shell commands, guidance] <br>
**Output Format:** [Spoken audio playback with concise text status and inline bash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local TTS playback, temporary audio files, and public URL text extraction when requested.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
