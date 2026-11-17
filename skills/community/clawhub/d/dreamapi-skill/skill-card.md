## Description:

25 AI-powered tools for video generation, talking avatars, image editing, voice cloning, and more powered by DreamAPI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dream-api](https://clawhub.ai/user/dream-api)

### License/Terms of Use:

Apache 2.0

## Use Case:

External users and developers use this skill to have an AI agent generate or edit images, video, avatars, translated video, and voice outputs through DreamAPI from natural-language requests and media inputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and uploaded media may be sent to DreamAPI for processing.

Mitigation: Use the skill only with media and prompts that are appropriate to share with DreamAPI.

Risk: Face swap, voice clone, lip-sync translation, and watermark removal can involve sensitive identity or rights issues.

Mitigation: Use only media you have rights and consent to process, and review these requests before execution.

Risk: API keys may be exposed if pasted into chat, command lines, or plaintext credential files.

Mitigation: Prefer a protected environment secret and avoid sharing API keys in chat or shell history.

## Reference(s):

- [DreamAPI Skill README](README.md)
- [DreamAPI API Docs](https://api.newportai.com/api-docs)
- [DreamAPI Dashboard](https://api.newportai.com/)
- [Authentication](references/auth.md)
- [Avatar](references/avatar.md)
- [Image Generation](references/image_gen.md)
- [Image Editing](references/image_edit.md)
- [Video Generation](references/video_gen.md)
- [Video Editing](references/video_edit.md)
- [Video Translate](references/video_translate.md)
- [Voice](references/voice.md)
- [Polling](references/polling.md)
- [Storage](references/storage.md)
- [Error Handling](references/error_handling.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and result links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return image, video, and audio URLs, clone IDs, task metadata, or account credit information.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
