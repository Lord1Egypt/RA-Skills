## Description: <br>
抖音视频下载工具。当用户要求下载抖音（豆包）短视频时使用此 skill。支持短链接（如 v.douyin.com/xxx）和完整视频页面链接，自动解析并下载到本地。下载视频为 720p 带水印版本。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maxdong-max](https://clawhub.ai/user/maxdong-max) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and external users can ask an agent to resolve Douyin short or full video links, fetch the mobile page, and download the requested 720p watermarked MP4 to local disk. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts Douyin-related endpoints and saves requested videos on the local machine. <br>
Mitigation: Use the skill only for explicit download requests, check the saved filename and path, and store only content the user is allowed and comfortable keeping locally. <br>
Risk: A failed or stale Douyin request can produce a small error page instead of a valid MP4. <br>
Mitigation: Verify the downloaded file size and format after each download, then retry with a freshly resolved video ID if the output is invalid. <br>


## Reference(s): <br>
- [Douyin API Reference](douyin_api.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/maxdong-max/douyin-download-china) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and saved MP4 files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Downloads requested videos to ~/Downloads and verifies file size and format.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
