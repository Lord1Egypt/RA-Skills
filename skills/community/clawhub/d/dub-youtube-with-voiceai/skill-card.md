## Description: <br>
Dub YouTube videos with Voice.ai TTS. Turn scripts into publish-ready voiceovers with chapters, captions, and audio replacement for YouTube long-form and Shorts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gizmoGremlin](https://clawhub.ai/user/gizmoGremlin) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External creators and developers use this skill to turn scripts into YouTube-ready AI voiceovers, captions, chapters, review pages, and optional dubbed video files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected script text is sent to Voice.ai or to the endpoint configured with VOICEAI_API_BASE. <br>
Mitigation: Use only approved script content, avoid sensitive or regulated text unless authorized, and keep VOICEAI_API_BASE unset unless an alternate endpoint is intentionally required. <br>
Risk: A Voice.ai API key is required for non-mock generation. <br>
Mitigation: Use a dedicated, revocable API key and rotate it if exposed. <br>
Risk: Generated ffmpeg helper scripts may be run manually. <br>
Mitigation: Review generated helper scripts before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gizmoGremlin/dub-youtube-with-voiceai) <br>
- [Voice.ai API Reference](references/VOICEAI_API.md) <br>
- [Troubleshooting](references/TROUBLESHOOTING.md) <br>
- [Voice.ai](https://voice.ai) <br>
- [Agent Skills Specification](https://agentskills.io/specification) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Configuration, Markdown, Text] <br>
**Output Format:** [Markdown guidance with CLI commands; generated artifacts include WAV, MP3, MP4, SRT, JSON, HTML, and text files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses VOICE_AI_API_KEY for Voice.ai requests; ffmpeg is optional but required for audio stitching, MP3 encoding, normalization, and video dubbing.] <br>

## Skill Version(s): <br>
0.1.6 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
