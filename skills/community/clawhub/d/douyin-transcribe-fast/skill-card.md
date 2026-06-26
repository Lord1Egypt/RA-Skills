## Description: <br>
抖音视频快速转文字 helps agents turn Douyin links or local video files into Chinese transcripts using ffmpeg and local Whisper. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[btboy773](https://clawhub.ai/user/btboy773) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to process Douyin links or local video files, extract audio, and return Chinese transcript text. It is aimed at low-cost local transcription workflows where users can install Python, ffmpeg, and Whisper. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The helper can execute shell commands built from user-supplied Douyin links or file paths. <br>
Mitigation: Use trusted links and file paths only; prefer a revised helper that passes subprocess arguments as lists, validates inputs, and avoids shell=True. <br>
Risk: Douyin-link processing may require network access, so the privacy and offline claims are incomplete. <br>
Mitigation: Treat Douyin links as networked processing, review what is sent to douyin-mcp and ffmpeg, and use local video files for stricter privacy. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/btboy773/douyin-transcribe-fast) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with inline shell commands and plain-text transcript output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The bundled helper may write transcript .txt files under ~/.openclaw/workspace/douyin-transcripts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
