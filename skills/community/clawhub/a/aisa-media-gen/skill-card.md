## Description:

Generate images and videos with AIsa using Gemini 3 Pro Image for images and Qwen Wan 2.6 for video through one API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aisapay](https://clawhub.ai/user/aisapay)

### License/Terms of Use:


## Use Case:

Developers and content teams use this skill to call AIsa image and video generation APIs from agent workflows, including creating images, starting video tasks, checking task status, and downloading completed videos.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The video download helper can fetch and save an unvalidated URL returned by the API.

Mitigation: Use --download only when the returned media source is trusted, and review the task result before saving media locally.

Risk: Prompts, reference image URLs, and API credentials are sent to AIsa services.

Mitigation: Use the skill only when AIsa is trusted for the submitted content, and prefer AISA_API_KEY over passing credentials on the command line.

Risk: The client can overwrite files at user-selected output paths.

Mitigation: Choose output paths carefully and avoid writing into sensitive directories or over existing files.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/aisapay/skills/aisa-media-gen)
- [AIsa API Reference](https://aisa.mintlify.app/api-reference/introduction)
- [AIsa Gemini GenerateContent API](https://aisa.mintlify.app/api-reference/chat/chat-api/google-gemini-chat.md)
- [AIsa Video Generation API](https://aisa.mintlify.app/api-reference/aliyun/video/video-generation.md)
- [AIsa Video Task API](https://aisa.mintlify.app/api-reference/aliyun/video/task.md)
- [OpenClaw](https://openclaw.ai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, API calls, Files]

**Output Format:** [Markdown guidance with shell commands, Python client usage, JSON API responses, and generated media files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AISA_API_KEY; image output may be saved as PNG, JPG, or WebP, and video output may be saved as MP4 when download is enabled.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
