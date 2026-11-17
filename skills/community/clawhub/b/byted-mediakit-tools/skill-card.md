## Description:

Byted Mediakit Tools helps agents use Volcengine AI MediaKit and Ark services for video understanding, audio extraction, media trimming, media concatenation, video enhancement, image-to-video generation, audio-video muxing, and asynchronous task status checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[volc-ai-mediakit](https://clawhub.ai/user/volc-ai-mediakit)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to invoke cloud media-processing workflows for user-supplied audio, video, and image URLs, then return task identifiers, processing status, generated media URLs, or video-understanding text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys may be written to or retained in a local .env file.

Mitigation: Use platform-managed secrets or process-scoped environment variables for AMK_API_KEY and ARK_API_KEY, and do not commit real credentials to the skill directory.

Risk: The skill submits media URLs to external Volcengine or Ark services for processing.

Mitigation: Use only media URLs approved for external processing, avoid confidential or personal media unless authorized, and rotate credentials that may have been stored or shared.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/volc-ai-mediakit/skills/byted-mediakit-tools)
- [AI MediaKit console](https://console.volcengine.com/imp/ai-mediakit/)
- [Ark model and key console](https://console.volcengine.com/ark/region:ark+cn-beijing/model/detail?Id=doubao-seed-1-8)
- [Common response format](reference/common_response.md)
- [Video understanding](reference/understand_video_content.md)
- [Task status query](reference/query_task.md)
- [Media concatenation](reference/concat_media_segments.md)
- [Video enhancement](reference/enhance_video.md)
- [Audio extraction](reference/extract_audio.md)
- [Image to video](reference/image_to_video.md)
- [Audio-video muxing](reference/mux_audio_video.md)
- [Media trimming](reference/trim_media_duration.md)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [JSON responses and concise Markdown guidance with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Media-processing outputs may include task_id, request_id, status, duration, and download-only play_url fields.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
