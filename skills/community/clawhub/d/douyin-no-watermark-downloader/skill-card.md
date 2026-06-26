## Description: <br>
下载抖音视频到本地（无水印），以mp4格式默认保存在桌面目录。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lvleiai123](https://clawhub.ai/user/lvleiai123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to download a public Douyin share link or share text as a local no-watermark MP4 file. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Douyin share links are sent to the lvhomeproxy2.dpdns.org resolver before the video is downloaded. <br>
Mitigation: Use only public links with user consent, and prefer a version that clearly documents the resolver before any network request is made. <br>
Risk: The workflow saves files returned through the resolver-backed download path to the user's Desktop. <br>
Mitigation: Validate returned download URLs, check file type and size before writing, and allow the user to choose the output folder. <br>


## Reference(s): <br>
- [ClawHub skill release](https://clawhub.ai/lvleiai123/douyin-no-watermark-downloader) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Text, Files] <br>
**Output Format:** [Terminal text with a downloaded MP4 file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Downloads the first resolved video URL to the user's Desktop as an .mp4 file.] <br>

## Skill Version(s): <br>
1.0.8 (source: release evidence and frontmatter metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
