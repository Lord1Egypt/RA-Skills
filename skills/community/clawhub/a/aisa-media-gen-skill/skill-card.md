## Description: <br>
Generate images and videos with AIsa using Gemini 3 Pro Image for images and Qwen Wan 2.6 for video through one API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bowen-dotcom](https://clawhub.ai/user/bowen-dotcom) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content automation agents use this skill to generate image files, create AIsa video generation tasks, poll task status, and optionally download generated videos. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends prompts, reference image URLs, and an API key-authorized request to AIsa. <br>
Mitigation: Use only approved prompts and media URLs, and do not submit secrets, private prompts, or sensitive image URLs unless approved for that provider. <br>
Risk: Generated image or video downloads can write to local output paths. <br>
Mitigation: Choose output paths carefully and review generated files before sharing or using them in downstream workflows. <br>
Risk: Automatic video download trusts the provider-returned download URL. <br>
Mitigation: Treat automatic video download as less hardened and use it only when the AIsa task response is trusted. <br>


## Reference(s): <br>
- [Skill page](https://clawhub.ai/bowen-dotcom/aisa-media-gen-skill) <br>
- [AIsa API Reference](https://docs.aisa.one/reference/) <br>
- [AIsa GenerateContent API](https://docs.aisa.one/reference/generatecontent) <br>
- [AIsa video generation API](https://docs.aisa.one/reference/post_services-aigc-video-generation-video-synthesis) <br>
- [AIsa task status API](https://docs.aisa.one/reference/get_services-aigc-tasks) <br>
- [OpenClaw](https://openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON API responses, and generated media files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AISA_API_KEY; image output is saved as png, jpg, or webp, and optional video download saves mp4 files.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
