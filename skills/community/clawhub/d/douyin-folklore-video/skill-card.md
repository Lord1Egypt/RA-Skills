## Description: <br>
抖音民间诡异故事视频生成器。根据用户提供的文案自动生成配音、图片、视频并合成最终视频，支持上传到抖音。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[google696](https://clawhub.ai/user/google696) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators and automation-focused developers use this skill to turn provided Chinese folklore or eerie-story text into short Douyin-style videos with narration, generated imagery, video clips, subtitles, and optional upload after user approval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Story text and generated media are sent to DashScope and to the configured FTP/HTTP host. <br>
Mitigation: Use dedicated API and FTP credentials, avoid sensitive unpublished material, and confirm the configured hosts before running generation. <br>
Risk: The Douyin upload path depends on an authenticated browser profile. <br>
Mitigation: Verify the openclaw browser profile is logged into the intended Douyin account before upload. <br>
Risk: Generated videos may contain unsuitable or inaccurate AI-generated content. <br>
Mitigation: Review the final video, title, description, topics, and AI disclosure before confirming publication. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/google696/douyin-folklore-video) <br>
- [Publisher profile](https://clawhub.ai/user/google696) <br>
- [Configuration reference](references/config.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and generated media file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces voice.wav, generated images, video segments, subtitle.srt, video_raw.mp4, video_sub.mp4, and final_video.mp4 when the required services and tools are configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
