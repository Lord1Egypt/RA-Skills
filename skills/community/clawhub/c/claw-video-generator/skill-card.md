## Description: <br>
Generate Pinterest-optimized vertical videos using JSON2Video API with AI-generated or URL-based images, AI-generated or provided voiceovers, optional subtitles, and zoom effects. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[benhuebner01](https://clawhub.ai/user/benhuebner01) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External creators, marketers, and automation developers use this skill to generate vertical social media videos from JSON scene configurations, including image, voiceover, subtitle, overlay, and render settings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Video prompts, narration text, overlays, image URLs, audio URLs, and related metadata are sent to JSON2Video. <br>
Mitigation: Do not include secrets, confidential business data, personal data, or private internal URLs in video configurations. <br>
Risk: The helper script prints a truncated payload preview to stdout, which can expose user-provided text or media URLs in logs. <br>
Mitigation: Review configs before execution and avoid running with sensitive content in shared terminals, CI logs, or retained logs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/benhuebner01/claw-video-generator) <br>
- [JSON2Video API key setup](https://json2video.com/get-api-key/) <br>
- [Azure Speech voices](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/language-support?tabs=tts) <br>
- [ElevenLabs Voice Library](https://elevenlabs.io/app/voice-library) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON configuration examples and Python or shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces JSON2Video render payloads and returns a project ID or video URL when the helper script is executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
