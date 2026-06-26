## Description: <br>
Send native Feishu voice bubbles by converting text to OGG/Opus audio with edge-tts and ffmpeg for delivery through a Feishu message tool. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cxzcy](https://clawhub.ai/user/cxzcy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to create playable Feishu voice-message replies when a user requests voice output or when a Feishu workflow needs text-to-speech delivery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Crafted voice, rate, or output-path values may lead to unsafe local shell execution or file overwrites in the helper script. <br>
Mitigation: Use only trusted prompts and confirmed Feishu destinations; prefer a fixed version that uses spawn or execFile argument arrays, validates voice and rate values, and restricts output paths to a safe temporary directory without silent overwrites. <br>
Risk: Generated temporary audio files are stored under /tmp and are not automatically cleaned up. <br>
Mitigation: Remove generated audio after message delivery and avoid placing sensitive speech content in persistent or shared temporary locations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cxzcy/feishu-voice-bot) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and generated audio file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces OGG/Opus audio paths for Feishu message-tool delivery; requires edge-tts, ffmpeg, and a Feishu message channel.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
