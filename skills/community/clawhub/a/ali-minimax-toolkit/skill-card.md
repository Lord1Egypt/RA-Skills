## Description:

MiniMax multimodal generation via API for voice, music, image, image-to-image, and video generation using cross-platform Python scripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuan-huicheng](https://clawhub.ai/user/yuan-huicheng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to generate speech, music, images, image variations, and videos through MiniMax APIs, then save generated media files for downstream workflows. It is suited to multimodal content generation tasks where prompts and selected input media can be sent to MiniMax.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, portraits, voice samples, and other selected media may be sent to MiniMax or to a custom API host.

Mitigation: Use the default trusted MiniMax host unless a custom endpoint is explicitly trusted, and avoid uploading confidential or non-consensual media.

Risk: The MiniMax API key is used for outbound API requests.

Mitigation: Keep MINIMAX_API_KEY private, scope and rotate it according to local policy, and do not expose it in logs, prompts, or shared artifacts.

## Reference(s):

- [MiniMax Image Generation API (image-01)](references/image-api.md)
- [MiniMax Music Generation API (music-2.5)](references/music-api.md)
- [TTS Guide](references/tts-guide.md)
- [TTS Voice Catalog](references/tts-voice-catalog.md)
- [MiniMax Video Generation API Documentation](references/video-api.md)
- [Video Prompt Writing Guide](references/video-prompt-guide.md)
- [MiniMax image generation documentation](https://platform.minimaxi.com/docs/api-reference/image-generation-t2i)
- [MiniMax image-to-image documentation](https://platform.minimaxi.com/docs/api-reference/image-generation-i2i)
- [MiniMax music generation documentation](https://platform.minimaxi.com/docs/api-reference/music-generation)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with Python snippets, shell commands, and generated media file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated media is saved under minimax-output/ by convention; Feishu delivery is represented as follow-up send instructions when requested.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
