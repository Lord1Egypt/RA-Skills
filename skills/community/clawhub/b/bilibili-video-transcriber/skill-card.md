## Description: <br>
Transcribes Bilibili videos by retrieving available subtitles or converting audio, with support for comments, summaries, and optional Feishu/Lark document creation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[adolescen-he](https://clawhub.ai/user/adolescen-he) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and content reviewers use this skill to turn Bilibili video IDs or URLs into transcripts, structured metadata, summaries, and popular-comment extracts for review or downstream analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles Bilibili session cookies and may store or synchronize them across multiple local paths. <br>
Mitigation: Remove bundled cookie files before use, prefer a low-privilege Bilibili account, and verify cookie storage paths and file permissions. <br>
Risk: Transcripts, video metadata, comments, or login-related artifacts may be sent to Feishu/Lark when that integration is configured. <br>
Mitigation: Disable or patch automatic Feishu/Lark document creation when local-only processing is required, and review any lark-cli configuration before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/adolescen-he/bilibili-video-transcriber) <br>
- [Publisher profile](https://clawhub.ai/user/adolescen-he) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, JSON, and plain-text transcript artifacts with CLI commands and configuration examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include video metadata, timed transcript segments, popular comments, cookie status, and optional Feishu/Lark document URLs.] <br>

## Skill Version(s): <br>
2.4.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
