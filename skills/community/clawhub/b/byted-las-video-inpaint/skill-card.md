## Description: <br>
Removes watermarks, subtitles, logos, text overlays, and other fixed-region visual artifacts from video using Volcengine LAS video inpainting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[volcengine-skills](https://clawhub.ai/user/volcengine-skills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and video operations teams use this skill to submit Volcengine LAS video-inpainting jobs, estimate cost, poll task status, and return cleaned video output paths. <br>

### Deployment Geography for Use: <br>
Global, subject to Volcengine LAS regional availability. <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires cloud credentials and sends selected videos or presigned links to Volcengine LAS. <br>
Mitigation: Use dedicated least-privileged LAS and TOS credentials, keep env.sh and .env out of version control, and process only videos approved for that cloud workflow. <br>
Risk: Initial setup may download and install the LAS SDK at runtime. <br>
Mitigation: Run first setup in an isolated workspace and install only when the user trusts Volcengine LAS and the referenced SDK source. <br>
Risk: Region or output TOS path mismatches can cause upload, permission, or result delivery failures. <br>
Mitigation: Confirm LAS_REGION, API key scope, and the writable output_tos_path before submitting a job. <br>
Risk: Video watermark, logo, subtitle, or overlay removal can be misused on content the user is not authorized to modify. <br>
Mitigation: Confirm the user has the right to modify the video and obtain explicit confirmation before submitting paid inpainting work. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/volcengine-skills/byted-las-video-inpaint) <br>
- [las_video_inpaint API reference](artifact/references/api.md) <br>
- [Volcengine LAS pricing](https://www.volcengine.com/docs/6492/1544808) <br>
- [Skill pricing reference](artifact/references/prices.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, JSON, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include task IDs, TOS paths, presigned URLs, local output paths, and price estimates.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
