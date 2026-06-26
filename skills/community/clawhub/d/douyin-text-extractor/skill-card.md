## Description: <br>
Extracts Douyin video metadata, no-watermark download links, and AI-generated speech transcripts through CLI, Python, and MCP workflows using SiliconFlow or Aliyun transcription APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rfdiosuao](https://clawhub.ai/user/rfdiosuao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, social media operators, and developers use this skill to retrieve Douyin video information, download video assets, and generate transcript text for content analysis or agent workflows. Transcription requires a configured SiliconFlow or Aliyun API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The FFmpeg installer can download and run unverified binary artifacts. <br>
Mitigation: Prefer a trusted package manager or manually verify downloaded FFmpeg binaries before running the installer. <br>
Risk: Video URLs, downloaded media, or extracted audio may be sent to third-party transcription services. <br>
Mitigation: Use the skill only with content you are comfortable sending to SiliconFlow or Aliyun, and review those services' terms before use. <br>
Risk: API keys are required for transcription and MCP use. <br>
Mitigation: Use limited-scope keys, provide them through environment variables, and rotate them if they are exposed. <br>
Risk: MCP tools can download media and process external URLs when invoked by a connected client. <br>
Mitigation: Configure the MCP server only for trusted clients and review requested Douyin URLs before tool execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/rfdiosuao/douyin-text-extractor) <br>
- [SiliconFlow API documentation](https://docs.siliconflow.cn/) <br>
- [SiliconFlow registration link](https://cloud.siliconflow.cn/i/84kySW0S) <br>
- [FFmpeg downloads](https://ffmpeg.org/download.html) <br>
- [Aliyun DashScope console](https://dashscope.console.aliyun.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Plain text tool responses, Markdown transcript files, and command/configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs can include video metadata, download links, transcript.md files, and local media file paths.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
