## Description: <br>
Generate videos with Model Studio DashScope SDK using Wan i2v models (wan2.6-i2v-flash, wan2.6-i2v, wan2.6-i2v-us). Use when implementing or documenting video.generate requests/responses, mapping prompt/negative_prompt/duration/fps/size/seed/reference_image/motion_strength, or integrating video generation into the video-agent pipeline. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cinience](https://clawhub.ai/user/cinience) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and video-agent integrators use this skill to generate or document Alibaba Cloud DashScope Wan video requests, normalize video.generate parameters, poll asynchronous tasks, and save generated video outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends prompts and local reference images to Alibaba Cloud DashScope for generation. <br>
Mitigation: Use a dedicated DashScope API key and avoid private or regulated prompts and images unless approved for that provider. <br>
Risk: Generated-media URLs, task IDs, and polling responses can remain in local output directories. <br>
Mitigation: Periodically clean saved task logs and generated-media URLs from output directories. <br>
Risk: Video generation can take several minutes and may fail when required image-to-video inputs or supported sizes are missing. <br>
Mitigation: Use bounded polling with timeout, expose progress, validate reference_image and size before submission, and handle 4xx validation failures explicitly. <br>


## Reference(s): <br>
- [DashScope SDK Reference (Wan Video)](references/api_reference.md) <br>
- [Source List](references/sources.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, files] <br>
**Output Format:** [Markdown guidance with Python examples, JSON request and response shapes, shell commands, and generated video files when scripts are run] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires DASHSCOPE_API_KEY and may upload local reference images to Alibaba Cloud DashScope] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
