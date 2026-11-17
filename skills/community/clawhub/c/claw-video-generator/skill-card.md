## Description:

Generate Pinterest-optimized vertical videos using the JSON2Video API with AI-generated or URL-based images, generated or provided voiceovers, optional subtitles, and zoom effects.

This skill is ready for commercial/non-commercial use.

## Publisher:

[benhuebner01](https://clawhub.ai/user/benhuebner01)

### License/Terms of Use:


## Use Case:

Content creators, marketers, and developers use this skill to configure and generate vertical social videos for Pinterest and similar formats through the JSON2Video API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Video scripts, AI image prompts, voiceover text, public media URLs, and render metadata are sent to JSON2Video and any upstream providers used for media or AI generation.

Mitigation: Avoid secrets, private/internal URLs, confidential scripts, and sensitive prompts in video configs; review JSON2Video and upstream provider handling before use.

Risk: The skill requires a JSON2Video API key for external API calls.

Mitigation: Provide the key through the JSON2VIDEO_API_KEY environment variable and scope it to JSON2Video usage.

Risk: Provider-side caching may retain generated assets or render inputs longer than some workflows allow.

Mitigation: Disable or adjust caching where retention requirements are stricter.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/benhuebner01/skills/claw-video-generator)
- [JSON2Video API key setup](https://json2video.com/get-api-key/)
- [Microsoft Azure Speech voices](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/language-support?tabs=tts)
- [ElevenLabs voice library](https://elevenlabs.io/app/voice-library)
- [Advanced usage guide](ADVANCED.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON configuration examples, Python code, shell commands, and API-returned project IDs or video URLs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces JSON2Video render requests from user-supplied scene, image, voice, subtitle, and quality settings.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
