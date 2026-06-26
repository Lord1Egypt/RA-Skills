## Description: <br>
Generate animated conversation videos with multi-voice TTS audio and timed text overlays. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pratyushchauhan](https://clawhub.ai/user/pratyushchauhan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content builders use this skill to turn dialogue manifests into podcast-style or interview-style conversation videos with synthesized multi-speaker audio, timed captions, and optional Remotion animation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated audio, timing JSON, terminal logs, and temporary WAV files may contain transcript text or other sensitive spoken content. <br>
Mitigation: Review transcript contents before use and handle generated media, timing files, logs, and temporary files according to the sensitivity of the source dialogue. <br>
Risk: The skill runs local media-generation commands and may require npm install for the optional Remotion template. <br>
Mitigation: Install and run it only in an environment where local command execution and package installation are acceptable, and review dependencies before rendering. <br>


## Reference(s): <br>
- [FFmpeg Text Overlay Guide](references/ffmpeg-guide.md) <br>
- [Remotion Patterns Reference](references/remotion-patterns.md) <br>
- [Conversation Video on ClawHub](https://clawhub.ai/pratyushchauhan/conversation-video) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with JSON manifest examples, Python and ffmpeg commands, and optional Remotion code edits; executed scripts produce WAV audio, JSON timing data, and MP4 video files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local ffmpeg and Supertonic TTS for the audio path; the optional Remotion path requires Node.js and npm.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
