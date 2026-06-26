## Description: <br>
抖音无水印视频下载器，支持分享链接解析、批量下载和元数据保存。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chall2015](https://clawhub.ai/user/chall2015) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to parse public Douyin links, download videos, and optionally save local metadata for personal media workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill downloads public Douyin content and saves media plus optional metadata locally. <br>
Mitigation: Set an explicit save directory, disable metadata when it is not needed, and review downloaded files before reuse or redistribution. <br>
Risk: The skill runs Playwright/Chromium and may create debug screenshots during browser extraction. <br>
Mitigation: Run it in a controlled environment and remove or gate debug screenshot behavior before routine use. <br>
Risk: Large batch downloads can trigger service rate limits or unwanted local storage growth. <br>
Mitigation: Keep concurrency low, avoid large batches, and monitor the configured output directory. <br>
Risk: Dependency and transparency issues were noted by the security scan. <br>
Mitigation: Update or pin dependencies and review the package contents before installing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chall2015/douyin-downloader-latest) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown status messages with file paths, JSON metadata, JavaScript APIs, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save MP4 media files and optional JSON metadata to a configured local directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
