## Description: <br>
Generate images and videos with AIsa using Gemini 3 Pro Image for image generation and Qwen Wan 2.6 for video generation through one API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AIsaPay](https://clawhub.ai/user/AIsaPay) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and creators use this skill to generate images and create, poll, and optionally download video generation tasks through AIsa using one API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, referenced image URLs, and the AISA_API_KEY are sent to AIsa when the helper is invoked. <br>
Mitigation: Install only when the user trusts AIsa and the publisher, and avoid submitting secrets, private URLs, or regulated personal data. <br>
Risk: Generated images and downloaded videos may write or overwrite local output files. <br>
Mitigation: Use explicit, safe output paths and review paths before running commands that save media locally. <br>


## Reference(s): <br>
- [AIsa API Reference](https://aisa.mintlify.app/api-reference/introduction) <br>
- [AIsa Gemini GenerateContent API](https://aisa.mintlify.app/api-reference/chat/chat-api/google-gemini-chat.md) <br>
- [AIsa Video Generation API](https://aisa.mintlify.app/api-reference/aliyun/video/video-generation.md) <br>
- [AIsa Video Task API](https://aisa.mintlify.app/api-reference/aliyun/video/task.md) <br>
- [ClawHub skill page](https://clawhub.ai/AIsaPay/aisa-media-gen) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and Python client examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated media may be saved to local image or MP4 files when the Python helper is invoked.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
