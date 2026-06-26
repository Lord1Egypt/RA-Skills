## Description: <br>
25 AI-powered tools for video generation, talking avatars, image editing, voice cloning, and more - powered by DreamAPI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dream-api](https://clawhub.ai/user/dream-api) <br>

### License/Terms of Use: <br>
Apache 2.0 <br>


## Use Case: <br>
External users and developers use this skill to ask an agent for DreamAPI media workflows, including image generation and editing, video generation and editing, avatar creation, video translation, text-to-speech, voice cloning, and account credit checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uploads prompts and user-provided image, audio, or video files to a third-party DreamAPI/Newport AI service. <br>
Mitigation: Use it only with content the user has rights and consent to process, and avoid private, confidential, third-party, biometric face, voice, or video content unless approval is explicit. <br>
Risk: The skill requires a DreamAPI API key and can consume account credits while running multi-step media jobs. <br>
Mitigation: Use a revocable key, review account credit use, and ask the agent to confirm before uploads, purchases, or multi-step generation workflows. <br>
Risk: The skill includes face, voice, watermark, and media manipulation capabilities that can be misused or produce content requiring rights review. <br>
Mitigation: Confirm authorization for likeness, voice, watermark, and source media before generation, editing, or publication. <br>


## Reference(s): <br>
- [DreamAPI API Docs](https://api.newportai.com/api-docs) <br>
- [DreamAPI Dashboard](https://api.newportai.com/) <br>
- [Agent Skills Specification](https://agentskills.io/specification) <br>
- [Authentication](references/auth.md) <br>
- [Avatar](references/avatar.md) <br>
- [Image Generation](references/image_gen.md) <br>
- [Image Editing](references/image_edit.md) <br>
- [Video Generation](references/video_gen.md) <br>
- [Video Editing](references/video_edit.md) <br>
- [Video Translate](references/video_translate.md) <br>
- [Voice](references/voice.md) <br>
- [Polling](references/polling.md) <br>
- [Storage](references/storage.md) <br>
- [User](references/user.md) <br>
- [Error Handling](references/error_handling.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, media URLs] <br>
**Output Format:** [Markdown and concise text responses with command guidance, configuration steps, and generated media links.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require a DreamAPI API key, paid credits, local media uploads, asynchronous polling, and returned image, audio, or video URLs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
