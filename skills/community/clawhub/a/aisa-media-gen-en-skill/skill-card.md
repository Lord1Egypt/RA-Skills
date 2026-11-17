## Description:

Generate images and videos with AIsa using Gemini 3 Pro Image for image generation and Qwen Wan 2.6 for video generation via one API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bowen-dotcom](https://clawhub.ai/user/bowen-dotcom)

### License/Terms of Use:


## Use Case:

Developers, content creators, and agent builders use this skill to generate images, create asynchronous video tasks, poll video task status, and save generated media through the AIsa API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends prompts, reference image URLs, task IDs, and the AIsa API key to the external AIsa service.

Mitigation: Use AISA_API_KEY rather than passing keys on the command line, avoid sensitive prompts or private image URLs, and confirm that use of AIsa is approved for the target workload.

Risk: The optional video download path fetches a video URL returned by the external service and writes it to disk.

Mitigation: Use --download only for trusted tasks, choose output paths deliberately, and review downloaded media before reuse or distribution.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/bowen-dotcom/skills/aisa-media-gen-en-skill)
- [OpenClaw](https://openclaw.ai)
- [AIsa API Reference](https://aisa.mintlify.app/api-reference/introduction)
- [AIsa LLMs Documentation Index](https://aisa.mintlify.app/llms.txt)
- [Gemini GenerateContent Documentation](https://aisa.mintlify.app/api-reference/chat/chat-api/google-gemini-chat.md)
- [AIsa Video Generation Documentation](https://aisa.mintlify.app/api-reference/aliyun/video/video-generation.md)
- [AIsa Video Task Documentation](https://aisa.mintlify.app/api-reference/aliyun/video/task.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with shell commands, Python client invocations, JSON API responses, and generated media files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write image files and optionally download generated video files to local paths.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
