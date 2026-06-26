## Description: <br>
BizyAir 文件上传助手帮助用户将本地图片、音频、视频等资源上传到 BizyAir 服务器，并获取可访问的 URL。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bozoyan](https://clawhub.ai/user/bozoyan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creators use this skill to upload selected local media files to BizyAir and retrieve URLs for BizyAir workflows. It can also list previously uploaded BizyAir input resources. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected local files are uploaded to BizyAir/Alibaba OSS. <br>
Mitigation: Upload only files intended for BizyAir use and review file paths before running the upload command. <br>
Risk: The BizyAir API key authorizes uploads and resource listing. <br>
Mitigation: Store the key in BIZYAIR_API_KEY or another trusted secret store and avoid pasting it into conversation. <br>
Risk: Listing resources may expose names and URLs of prior BizyAir input resources. <br>
Mitigation: Use the list feature only when those resource names and URLs are appropriate to disclose. <br>


## Reference(s): <br>
- [BizyAir API upload tutorial](https://docs.bizyair.cn/api/upload-tutorial.html) <br>
- [BizyAir API key console](https://bizyair.cn/user/api-key) <br>
- [ClawHub skill page](https://clawhub.ai/bozoyan/bizyair-upload) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with URLs, status messages, and optional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include uploaded resource URLs, object keys, resource IDs, and error guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
