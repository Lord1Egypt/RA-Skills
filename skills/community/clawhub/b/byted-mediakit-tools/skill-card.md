## Description: <br>
火山引擎 AI MediaKit 音视频处理工具集，提供视频理解、音频提取、视频剪辑、音视频拼接、画质增强、文生视频、音视频合成等能力。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[volc-ai-mediakit](https://clawhub.ai/user/volc-ai-mediakit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and media workflow operators use this skill to call Volcengine AI MediaKit services for video understanding, audio extraction, trimming, concatenation, enhancement, image-to-video generation, audio/video muxing, and task status queries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Media URLs and video-understanding prompts may be sent to external Volcengine or Ark services. <br>
Mitigation: Use only media and prompts approved for those services, and avoid private or internal URLs unless explicitly authorized. <br>
Risk: The skill can create a local .env template and may encourage storing real API keys in project files. <br>
Mitigation: Provide API keys through a secret manager or temporary environment variables, and avoid committing or sharing local .env files. <br>
Risk: Returned media links and task identifiers may expose generated or processed assets. <br>
Mitigation: Treat returned URLs, request IDs, and task IDs as sensitive and share them only with authorized recipients. <br>


## Reference(s): <br>
- [AI MediaKit Console](https://console.volcengine.com/imp/ai-mediakit/) <br>
- [Ark Model and Key Console](https://console.volcengine.com/ark/region:ark+cn-beijing/model/detail?Id=doubao-seed-1-8) <br>
- [Common Response Format](reference/common_response.md) <br>
- [Video Content Understanding](reference/understand_video_content.md) <br>
- [Query Task](reference/query_task.md) <br>
- [Concatenate Media Segments](reference/concat_media_segments.md) <br>
- [Enhance Video](reference/enhance_video.md) <br>
- [Extract Audio](reference/extract_audio.md) <br>
- [Image To Video](reference/image_to_video.md) <br>
- [Mux Audio Video](reference/mux_audio_video.md) <br>
- [Trim Media Duration](reference/trim_media_duration.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, JSON, API calls] <br>
**Output Format:** [Markdown instructions, shell commands, and JSON responses from media-processing API calls.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Asynchronous operations may return task identifiers and downloadable media URLs; video understanding returns model-generated text in JSON.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
