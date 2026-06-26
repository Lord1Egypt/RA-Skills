## Description: <br>
使用 Node.js 从抖音网页解析视频信息并下载，支持视频和图文类型 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xbos1314](https://clawhub.ai/user/xbos1314) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to parse Douyin links, download video or image-post media, and return structured details such as title, author, statistics, cover, image URLs, and video URL. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The downloader fetches media from user-provided Douyin links and writes files locally. <br>
Mitigation: Use trusted Douyin links and prefer the default or a dedicated empty output folder. <br>
Risk: A custom output directory could target sensitive project or system locations. <br>
Mitigation: Avoid pointing the output directory at sensitive paths and review downloaded files before reuse. <br>
Risk: Douyin media URLs are temporary and some content may require login or may not be accessible. <br>
Mitigation: Expect download failures or expired links and retry with accessible content when appropriate. <br>


## Reference(s): <br>
- [ClawHub listing: douyin-downloader-js](https://clawhub.ai/xbos1314/douyin-downloader-js) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, files, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON result structures] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Downloads media files to a local output directory; image posts are limited to the first three images with a remaining-count notice.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
