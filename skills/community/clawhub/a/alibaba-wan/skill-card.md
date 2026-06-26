## Description: <br>
Generates AI videos and images with Alibaba Wan 2.6 and Wan 2.5 through Atlas Cloud, including text-to-video, image-to-video, video-to-video, text-to-image, and image editing workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xixihhhh](https://clawhub.ai/user/xixihhhh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creators, and external users use this skill to select and run Alibaba Wan media-generation workflows through Atlas Cloud for video clips, image generation, image editing, and media transformations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes paid Atlas Cloud calls and uses an Atlas Cloud API key that the evidence says is broad in scope. <br>
Mitigation: Confirm provider, model, resolution, duration, and account billing before execution; protect and rotate the API key if exposed. <br>
Risk: Prompts and media can be sent to Atlas Cloud, and the image script can optionally use Google AI Studio when GEMINI_API_KEY is set. <br>
Mitigation: Avoid sending private prompts, images, audio, or videos unless approved; leave GEMINI_API_KEY unset unless Google AI Studio is intended and verify provider selection before generation. <br>
Risk: Upload commands can send local files to Atlas Cloud. <br>
Mitigation: Review file contents and upload intent before running upload commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xixihhhh/alibaba-wan) <br>
- [Atlas Cloud](https://www.atlascloud.ai) <br>
- [fal.ai Wan 2.6 text-to-video pricing reference](https://fal.ai/models/fal-ai/wan/v2.6/text-to-video) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Code, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and generated media file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call external media-generation APIs and download generated PNG or MP4 outputs to a user-selected directory.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
