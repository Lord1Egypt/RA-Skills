## Description: <br>
Wraps the Agnes AI API for image and video generation using OpenAI-compatible endpoints, with model guidance for text-to-image, image-to-image, multi-image composition, and asynchronous video generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[songxf1024](https://clawhub.ai/user/songxf1024) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to generate images or videos through Agnes AI from natural-language prompts, optional input images, and saved local output paths. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API keys are sensitive credentials and the skill can store AGNES_API_KEY in a local file. <br>
Mitigation: Prefer a session environment variable; when using ~/.agnes-ai/api_key, restrict file permissions and avoid exposing the key in chat, logs, or command history. <br>
Risk: Prompts and user-provided images may be sent to Agnes AI for generation. <br>
Mitigation: Use the skill only with content appropriate for Agnes AI processing, and avoid confidential images or private internal URLs unless the provider's handling and retention terms are acceptable. <br>


## Reference(s): <br>
- [Agnes AI API Reference](references/api.md) <br>
- [Agnes AI API Base](https://apihub.agnes-ai.com/v1) <br>
- [ClawHub skill page](https://clawhub.ai/songxf1024/agnes-ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and local image or video file outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses an Agnes AI API key and may upload prompts or user-provided images to Agnes AI; generated media is downloaded to local files.] <br>

## Skill Version(s): <br>
1.0.3 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
