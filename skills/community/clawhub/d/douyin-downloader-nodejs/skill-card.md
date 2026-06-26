## Description: <br>
抖音无水印视频下载和文案提取工具。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[whille](https://clawhub.ai/user/whille) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and content workflow users can use this skill to inspect Douyin share links, download watermark-free video files, and optionally extract speech transcripts with a SiliconFlow API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill downloads Douyin media to a local output directory. <br>
Mitigation: Choose the output directory deliberately and process only media you have permission to download. <br>
Risk: Transcript extraction sends extracted audio to SiliconFlow for transcription. <br>
Mitigation: Use a dedicated API key and avoid submitting audio that should not be shared with the transcription provider. <br>


## Reference(s): <br>
- [Douyin MCP Server homepage](https://github.com/yzfly/douyin-mcp-server) <br>
- [SiliconFlow API key portal](https://cloud.siliconflow.cn/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, files] <br>
**Output Format:** [Command-line output and optional Markdown transcript files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ffmpeg for media processing; transcript extraction requires DOUYIN_API_KEY or API_KEY.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
