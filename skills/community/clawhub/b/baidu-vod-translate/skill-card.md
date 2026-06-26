## Description: <br>
百度智能云VOD视频翻译工具，帮助代理通过 Baidu VOD 处理视频字幕翻译、语音翻译和配音，并支持批量处理、字幕样式配置、本地下载和可选网盘上传。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lhx121619](https://clawhub.ai/user/lhx121619) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to guide an agent through Baidu VOD video translation workflows, including collecting parameters, confirming execution, and running Python commands for subtitle translation, speech translation, task management, and result retrieval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uploads selected videos, subtitles, and speech content to Baidu cloud services for paid VOD processing. <br>
Mitigation: Use non-sensitive media for testing, confirm user consent before upload, and review Baidu pricing and data handling expectations before running translation tasks. <br>
Risk: The scripts use Baidu Access Key and Secret Key credentials and can create, query, update, and delete VOD projects and tasks. <br>
Mitigation: Use credentials with the least necessary Baidu permissions, keep credentials in environment variables only, and verify project and task IDs before management operations. <br>
Risk: The artifact includes project deletion capability that can remove cloud VOD project resources. <br>
Mitigation: Require an explicit user confirmation for deletion commands and inspect the exact project ID before execution. <br>
Risk: Optional netdisk workflows move processed media through the bdpan CLI. <br>
Mitigation: Confirm bdpan login state and destination paths before download or upload, and avoid using shared accounts for sensitive media. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lhx121619/skills/baidu-vod-translate) <br>
- [Baidu VOD video translation pricing](https://cloud.baidu.com/doc/VOD/s/Zmheig5gv) <br>
- [Baidu Intelligent VOD product](https://cloud.baidu.com/product/vod.html) <br>
- [Baidu VOD project management API](https://cloud.baidu.com/doc/VOD/s/Dmh0j7ldd) <br>
- [Baidu VOD task management API](https://cloud.baidu.com/doc/VOD/s/ymh0j93u8) <br>
- [Baidu Cloud access key management](https://console.bce.baidu.com/iam/#/iam/accesslist) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Code] <br>
**Output Format:** [Markdown guidance with inline shell commands and Python script invocation patterns] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and Baidu VOD credentials via BAIDU_VOD_AK and BAIDU_VOD_SK; optional bdpan CLI is used for netdisk workflows.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
