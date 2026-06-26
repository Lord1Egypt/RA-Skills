## Description: <br>
抖音视频获取模块。从抖音链接下载视频文件，支持短视频和 DASH 格式长视频。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[don068589](https://clawhub.ai/user/don068589) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to resolve Douyin video links, extract media stream URLs through a browser session, and download or merge short-form and DASH video assets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may use a browser profile and potentially rely on existing session credentials while accessing Douyin pages. <br>
Mitigation: Use a dedicated low-privilege browser profile and require explicit approval before using authenticated sessions or credentials. <br>
Risk: The workflow can download, merge, archive, move, and delete media files and transcripts. <br>
Mitigation: Confirm the source link, rights to download, output paths, retention choice, and cleanup actions before running file operations. <br>
Risk: Extracted audio may be sent to a local ASR endpoint for transcription. <br>
Mitigation: Confirm the ASR endpoint, data handling expectations, and whether the media contains sensitive content before transcription. <br>
Risk: The release evidence flags stale TikHub API behavior for review. <br>
Mitigation: Remove or review the TikHub API path before use and do not configure API tokens without explicit user approval. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/don068589/douyin-fetcher) <br>
- [Publisher profile](https://clawhub.ai/user/don068589) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, configuration] <br>
**Output Format:** [Markdown instructions with shell commands, browser actions, and JavaScript snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide creation of video, audio, merged media, and transcript files when the agent follows the workflow.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
