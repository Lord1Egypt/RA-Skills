## Description: <br>
Generates videos with Model Studio DashScope SDK using Wan video generation models and standardizes video.generate request and response handling for video-agent pipelines. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cinience](https://clawhub.ai/user/cinience) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and video-agent builders use this skill to call Alibaba Cloud DashScope Wan text-to-video and image-to-video models, normalize video.generate parameters, poll asynchronous jobs, and save generated video outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, reference images, generated media URLs, and output files may contain sensitive content. <br>
Mitigation: Use scoped DashScope credentials, avoid submitting sensitive inputs unless approved, and clean generated output files and logs when they contain sensitive content. <br>
Risk: Video generation sends requests and local reference images to Alibaba Cloud DashScope. <br>
Mitigation: Confirm the intended region, model, and data handling requirements before running generation jobs. <br>
Risk: Asynchronous video generation can run for several minutes and fail or time out. <br>
Mitigation: Use bounded polling, progress reporting, retry or resume behavior, and preserve task IDs for troubleshooting. <br>


## Reference(s): <br>
- [DashScope SDK Reference (Wan Video)](references/api_reference.md) <br>
- [Source List](references/sources.md) <br>
- [Model Studio Newly Released Models](https://help.aliyun.com/zh/model-studio/newly-released-models) <br>
- [Wan Text-to-Video Guide](https://help.aliyun.com/zh/model-studio/text-to-video-guide) <br>
- [Wan First-Frame Image-to-Video Guide](https://help.aliyun.com/zh/model-studio/first-frame-image-to-video) <br>
- [Model Studio Model List](https://help.aliyun.com/zh/model-studio/models) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with Python examples, shell commands, JSON request and response shapes, and generated media files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces normalized video_url, duration, fps, and seed values; scripts may download MP4 outputs and optional reference images to the configured output directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
