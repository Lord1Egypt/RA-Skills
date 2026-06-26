## Description: <br>
下载抖音视频到本地文件。当用户需要下载抖音视频、提取抖音链接内容、或保存抖音分享的视频时使用。支持抖音短链（v.douyin.com）、分享文本（含短链）、视频直链（douyin.com/video/...）三种输入格式。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wudi](https://clawhub.ai/user/wudi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to download supported Douyin video posts from a short link, pasted share text, or direct video URL and save the resulting MP4 locally. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts Douyin-related hosts and downloads media from the network. <br>
Mitigation: Install and run it only when you intend to download Douyin videos, and paste only links or share text you trust. <br>
Risk: The script writes an MP4 file to a user-selected or title-derived local path. <br>
Mitigation: Choose a safe output filename or folder and confirm it will not overwrite an important file. <br>
Risk: Unsupported Douyin content types such as image/text notes may not download. <br>
Mitigation: Use the skill for video posts and expect the script to notify the user when a supported video address is not available. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wudi/free-douyin-downloader) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Files] <br>
**Output Format:** [Markdown with inline bash code blocks and local MP4 file output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Python 3 standard library network requests to contact Douyin-related hosts and save an MP4 file locally.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
