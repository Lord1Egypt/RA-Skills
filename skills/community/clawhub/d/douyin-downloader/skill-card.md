## Description: <br>
最稳定的抖音视频下载工具，用户提供抖音链接或modal_id即可自动解析并下载。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[valderwu3](https://clawhub.ai/user/valderwu3) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Users with a Douyin link or modal_id use this skill to resolve a TikHub-backed video download URL and optionally download the video as an MP4 file. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a TikHub API token stored in a local OpenClaw configuration file. <br>
Mitigation: Use a dedicated revocable TikHub token, keep the config file private, and rotate the token if it may have been exposed. <br>
Risk: Douyin video identifiers are sent to TikHub to resolve video download URLs. <br>
Mitigation: Use the skill only when sharing those identifiers with TikHub is acceptable for the user and organization. <br>
Risk: Download mode writes an MP4 file to the working directory or requested output path. <br>
Mitigation: Check the downloaded file location after use and avoid overwriting important files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/valderwu3/douyin-downloader) <br>
- [TikHub token registration](https://user.tikhub.io/register?referral_code=JtYTGCqJ) <br>
- [TikHub Douyin video API](https://api.tikhub.io/api/v1/douyin/web/fetch_one_video) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Code, Shell commands, Configuration guidance, Files] <br>
**Output Format:** [Markdown guidance with Python command examples and MP4 files when download mode is used] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a TikHub API token stored in ~/.openclaw/config.json.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
